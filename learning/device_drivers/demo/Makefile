# Makefile
TARGET_MODULE:=demo

ifneq ($(KERNELRELEASE),)
	# Running by kernel build system
	$(TARGET_MODULE)-objs := main.o demo_device.o
	obj-m := $(TARGET_MODULE).o
else
	# Runnning without kernel build system
	BUILDSYSTEM_DIR := /lib/modules/$(shell uname -r)/build
	PWD := $(shell pwd)

all:
	$(MAKE) -C $(BUILDSYSTEM_DIR) M=$(PWD) modules
clean:
	$(MAKE) -C $(BUILDSYSTEM_DIR) M=$(PWD) clean 
load:
	sudo insmod ./$(TARGET_MODULE).ko
unload:
	sudo rmmod ./$(TARGET_MODULE).ko

endif
