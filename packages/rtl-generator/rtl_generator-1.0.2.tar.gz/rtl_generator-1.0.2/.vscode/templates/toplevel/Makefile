# defaults
SIM ?= #{simulator}
TOPLEVEL_LANG ?= #{hdl_lang}

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL ?= #{toplevel_name}

# MODULE is the basename of the Python test file
MODULE = test_$(TOPLEVEL)

VERILOG_SOURCES += $(PWD)/$(TOPLEVEL).#{hdl_ext}
# use VHDL_SOURCES for VHDL files

# Vivado project directory
VIVADO_PROJ_DIR ?= /media/$(USER)/EXT/vivado_rundir/$(TOPLEVEL)

# Testcases for this module when calling fst or vcd, leave empty for all
WAVE_TESTCASE ?=

# Conditionally include cocotb's make rules to take care of the simulator setup
ifneq ($(MAKECMDGOALS), rtl)
include $(shell cocotb-config --makefiles)/Makefile.sim
endif

.PHONY: rtl
rtl:
	python $gen_(TOPLEVEL).py $(RTL_ARGS)

.PHONY: vcd
vcd: export EXTRA_ARGS := --trace --trace-structs
vcd: 
ifdef TESTCASE
	$(MAKE) TESTCASE=$(TESTCASE)
else
	$(MAKE) TESTCASE=$(WAVE_TESTCASE)
endif
	cp -u dump.vcd $(TOPLEVEL).vcd && rm -f dump.vcd

.PHONY: fst
fst: export EXTRA_ARGS := --trace --trace-fst --trace-structs
fst:
ifdef TESTCASE
	$(MAKE) TESTCASE=$(TESTCASE)
else
	$(MAKE) TESTCASE=$(WAVE_TESTCASE)
endif
	cp -u dump.vcd $(TOPLEVEL).vcd && rm -f dump.vcd

PHONY: clean
clean::
	rm -f $(TOPLEVEL).vcd
	rm -f $(TOPLEVEL).fst
	rm -f results.xml
	rm -rf __pycache__