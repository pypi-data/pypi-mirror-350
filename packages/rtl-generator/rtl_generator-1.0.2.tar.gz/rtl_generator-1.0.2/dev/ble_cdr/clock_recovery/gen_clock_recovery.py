f"""
Generate Clock Recovery RTL code
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from rtl_generator import *
from gen_ble_cdr import *



# User-defined imports, functions, and globals
import numpy as np


def include_clock_recovery(existing_vars: dict) -> str:
    update_used_args(existing_vars, ["mf_clock_rec"])
    mf_clock_rec = existing_vars["mf_clock_rec"]
    rtl = matched_filter_clock_rec(existing_vars) if mf_clock_rec else paper_clock_rec(existing_vars)
    return rtl.strip("\n")

    
def matched_filter_clock_rec(existing_vars: dict) -> str:
    """
    Generate the matched filter clock recovery module
    """

    rtl = """
module clock_recovery # (
    parameter int SAMPLE_RATE = /* #{(samples_per_symbol)} */ 16 /* #{/(samples_per_symbol)} */
) (
    input logic clk,
    input logic en,
    input logic resetn,

    input logic mf_bit,
    
    output logic symbol_clk
);
    
    localparam int PIPELINE_STAGES = 1;
    
    logic [$clog2(SAMPLE_RATE-1):0] sample_counter;
    logic p_mf_bit;
    
    always_ff @(posedge clk or negedge resetn) begin
        if (~resetn) begin
            sample_counter <= 0;
            p_mf_bit <= 0;
        end else if (en) begin
            if ((mf_bit ^ p_mf_bit) || (sample_counter == SAMPLE_RATE - 1)) begin
                sample_counter <= 0;
            end else begin
                sample_counter <= sample_counter + 1;
            end
            
            p_mf_bit <= mf_bit;
        end
    end
    
    assign symbol_clk = (sample_counter == ((SAMPLE_RATE - 1) >> 1));
    
endmodule
    """.strip()

    return fill_in_template(rtl, existing_vars.get('args', None), existing_vars)


def paper_clock_rec(existing_vars: dict) -> str:
    """
    Generate the clock recovery module defined in 1990 paper
    """
    rtl = """
module clock_recovery # (
    parameter int SAMPLE_RATE = /* #{(samples_per_symbol)} */ 16 /* #{/(samples_per_symbol)} */,
    parameter int E_K_SHIFT = /* #{(ek_shift)} */ 2 /* #{/(ek_shift)} */,
    parameter int TAU_SHIFT = /* #{(tau_shift)} */ 11 /* #{/(tau_shift)} */,
    parameter int SAMPLE_POS = /* #{sample_pos)} */ 2 /* #{/(sample_pos)} */,
    parameter int DATA_WIDTH = /* #{(adc_width)} */ 4 /* #{/(adc_width)} */
    ) (
        input logic clk,
        input logic en,
        input logic resetn,
        
        input logic signed [DATA_WIDTH-1:0] i_data, q_data,
        input logic preamble_detected,
        
        output logic symbol_clk
        );
        
        localparam int PIPELINE_STAGES = 1;
        
        // Counter to schedule error calc due to preamble detection
        // Normally, error_calc_counter = 0, but when a preamble is detected, error_calc_counter = (SAMPLE_POS >> 1) + 1
        // Error calc is then scheduled to happen in the middle of the current symbol (when error_calc_counter == 1)
        logic [$clog2(SAMPLE_RATE):0] error_calc_counter, shift_counter;
        
        // Sample buffers to store samples used in error calculation
        // Samples are indexed as below, samples used are labeled with x. Start of symbol is marked with |, S is sample rate
        // S+2 S+1 S ... 2 1 0
        //  x   |  x     x | x
        localparam int BUFFER_SIZE = SAMPLE_RATE + 3;
        logic signed [BUFFER_SIZE-1:0][DATA_WIDTH-1:0] I_k, Q_k;
        
        // Variables to store the inputs to error calculation
        logic signed [DATA_WIDTH-1:0] i_1, q_1, i_2, q_2, i_3, q_3, i_4, q_4;
        
        // Variables to store error calculation results
        // #{(calculate_error_res)}
        localparam int  ERROR_RES = 18 + 0;
        // #{/(calculate_error_res)}
        localparam int TAU_RES = ERROR_RES - TAU_SHIFT;
        localparam int E_K_RES = ERROR_RES - E_K_SHIFT;
        localparam int D_TAU_RES = $clog2(SAMPLE_RATE + 1);
        logic signed [ERROR_RES-1:0] e_k, tau_int, tau_int_1, re1, re2, im1, im2, y1, y2;
        logic signed [E_K_RES-1:0] e_k_shifted;
        logic signed [TAU_RES-1:0] tau, tau_1;
        logic signed [D_TAU_RES-1:0] dtau;
        logic signed [ERROR_RES-1:0] i_1_sqr, q_1_sqr, i_2_sqr, q_2_sqr, i_3_sqr, q_3_sqr, i_4_sqr, q_4_sqr, iq_12, iq_34;
        
        integer re_correction = /* #{(re_correction)} */ 0 /* #{/(re_correction)} */;
        integer im_correction = /* #{(im_correction)} */ 0 /* #{/(im_correction)} */;
        logic do_error_calc;
        logic [D_TAU_RES-1:0] shift_counter_p1;
        
        always_comb begin
            // Combinational logic to assign buffer values to error calculation inputs
            i_1 = I_k[0 + SAMPLE_RATE];
            q_1 = Q_k[0 + SAMPLE_RATE];
            i_2 = I_k[0];
            q_2 = Q_k[0];
            i_3 = I_k[2 + SAMPLE_RATE];
            q_3 = Q_k[2 + SAMPLE_RATE];
            i_4 = I_k[2];
            q_4 = Q_k[2];
            
            // Combinational logic to compute error calculation
            i_1_sqr = i_1 * i_1;
            q_1_sqr = q_1 * q_1;
            i_2_sqr = i_2 * i_2;
            q_2_sqr = q_2 * q_2;
            i_3_sqr = i_3 * i_3;
            q_3_sqr = q_3 * q_3;
            i_4_sqr = i_4 * i_4;
            q_4_sqr = q_4 * q_4;
            iq_12 = i_1 * q_1 * i_2 * q_2;
            iq_34 = i_3 * q_3 * i_4 * q_4;
            
            re1 = (i_1_sqr - q_1_sqr) * (i_2_sqr - q_2_sqr) + (iq_12 << 2);
            re2 = (i_3_sqr - q_3_sqr) * (i_4_sqr - q_4_sqr) + (iq_34 << 2);
            im1 = ((i_2_sqr * i_1 * q_1) + (q_1_sqr * i_2 * q_2) - (i_1_sqr * i_2 * q_2) - (q_2_sqr * i_1 * q_1)) << 1;
            im2 = ((i_4_sqr * i_3 * q_3) + (q_3_sqr * i_4 * q_4) - (i_3_sqr * i_4 * q_4) - (q_4_sqr * i_3 * q_3)) << 1;
            
            // Compute y1 and y2 using correction factor
            y1 = (re_correction * re1) + (im_correction * im1);
            y2 = (re_correction * re2) + (im_correction * im2);
            
            // Compute error term
            e_k = y1 - y2;
            e_k_shifted = e_k[ERROR_RES-1:E_K_SHIFT];
            /* verilator lint_off WIDTHEXPAND */
            tau_int = tau_int_1 - e_k_shifted;
            /* verilator lint_on WIDTHEXPAND */
            tau = tau_int[ERROR_RES-1:TAU_SHIFT];
            
            // Determine if error calculation is scheduled
            shift_counter_p1 = (shift_counter + 1);
            do_error_calc = (error_calc_counter == 1) | (shift_counter_p1[D_TAU_RES-2:0] == dtau[D_TAU_RES-2:0]);
            
            // Output the symbol clock
            symbol_clk = (shift_counter == SAMPLE_POS);
        end
        
        always_ff @(posedge clk or negedge resetn) begin
            if (~resetn) begin
                tau_int_1 <= 0;
                tau_1 <= 0;
                dtau <= 0;
                shift_counter <= -PIPELINE_STAGES;
                error_calc_counter <= 0;
                I_k <= 0;
                Q_k <= 0;
        end else if (en) begin
            if (do_error_calc) begin
                // Store tau estimates and calculate dtau. Reset shift counter
                tau_int_1 <= tau_int;
                tau_1 <= tau;
                /* verilator lint_off WIDTHTRUNC */
                dtau <= (tau_1 - tau) >>> /* #{(correction_shift)} */ 0 /* #{/(correction_shift)} */;
                /* verilator lint_on WIDTHTRUNC */
                shift_counter <= 0;
            end else begin
                // Increment shift counter
                shift_counter <= shift_counter + 1;
            end
            
            // Decrement error calculation counter if error calculation is scheduled. Otherwise, schedule error calculation if preamble is detected
            if (error_calc_counter != 0) begin
                error_calc_counter <= error_calc_counter - 1;
            end else if (preamble_detected) begin
                error_calc_counter <= (SAMPLE_RATE >> 1) - SAMPLE_POS;
            end
            
            // Shift samples in buffer
            I_k <= {i_data, I_k[BUFFER_SIZE-1:1]};
            Q_k <= {q_data, Q_k[BUFFER_SIZE-1:1]};
        end
    end
    
endmodule
    """.strip()

    return fill_in_template(rtl, existing_vars.get('args', None), existing_vars)


def calculate_error_res(existing_vars: dict) -> str:
    return fill_in_template("localparam int ERROR_RES = #{(error_res)} + #{(correction_shift)};", existing_vars.get('args', None), existing_vars)


def error_res(existing_vars: dict) -> str:
    """
    Calculate the error resoultion
    """
    update_used_args(existing_vars, ['adc_width'])
    adc_width = existing_vars['adc_width']

    error_res = 2 * (2 * adc_width + 1)
    existing_vars['error_res'] = error_res
    return str(error_res)


def re_correction(existing_vars: dict) -> str:
    if callable(existing_vars['re_correction']):
        if_correction(existing_vars)

    return str(existing_vars['re_correction'])


def im_correction(existing_vars: dict) -> str:
    if callable(existing_vars['im_correction']):
        if_correction(existing_vars)

    return str(existing_vars['im_correction'])

def correction_shift(existing_vars: dict) -> str:
    if callable(existing_vars['correction_shift']):
        if_correction(existing_vars)

    return str(existing_vars['correction_shift'])


def if_correction(existing_vars: dict) -> None:
    """
    Compute the correction factor for the given intermediate frequency
    """
    update_used_args(existing_vars, ['fsym', 'clk_freq', 'ifreq'])
    symbol_rate = existing_vars['fsym']
    clk_freq = existing_vars['clk_freq']
    ifreq = existing_vars['ifreq']
    
    assert clk_freq % symbol_rate == 0, "Clock rate must be an integer multiple of symbol rate"
    samples_per_symbol = clk_freq // symbol_rate
    scum_if = ifreq / symbol_rate

    re_mult, im_mult = clock_recovery_if_correction(scum_if, samples_per_symbol)
    print(f'Correction coefficients: ({re_mult}, {im_mult})')

    # Scale the coefficients by powers of two until both are sufficiently close to an integer
    mults = np.array([re_mult, im_mult], dtype=np.float64)
    shift_amt = 0
    while np.max(np.abs(mults - mults.astype(int))) > 0.001:
        mults *= 2
        shift_amt += 1

    mults = mults.astype(int)

    print(f"Shift Amount: {shift_amt}")
    print(f"Final linear combination coefficients: ({mults[0]}, {mults[1]})")

    existing_vars['re_correction'] = mults[0]
    existing_vars['im_correction'] = mults[1]
    existing_vars['correction_shift'] = shift_amt
