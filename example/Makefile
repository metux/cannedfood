
INC_DIR=autogen/include

INCLUDE_FILES=\
    $(INC_DIR)/can_payload.h \
    $(INC_DIR)/can_messages.h \
    $(INC_DIR)/can_encode.h

GCH_FILES=$(addsuffix .gch,$(INCLUDE_FILES))

OBJS = \
    src/ecu_engine_control.o \
    autogen/src/nodes/ECU_ENGINE_CONTROL/recv_demux.o

all:	$(GCH_FILES) ecu_engine_control

$(INCLUDE_FILES):
	cd .. && ./run-example

%.h.gch: %.h
	$(CC) $< -I$(INC_DIR)

%.o: %.c
	$(CC) -c $< -o $@ -I$(INC_DIR) -Wall

ecu_engine_control: $(OBJS)
	$(CC) $(OBJS) -o $@ -I$(INC_DIR)

clean:
	@find -name "*.h.gch" -delete
	@find -name "*.o" -delete
	@rm -Rf autogen ecu_engine_control
