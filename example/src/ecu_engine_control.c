
#include <stdio.h>
#include <can_messages.h>
#include <nodes/ECU_ENGINE_CONTROL/recv_demux.h>
#include <linux/can.h>

int main()
{
    printf("hello world\n");
    struct can_frame fr = { 0 };
    node_ECU_ENGINE_CONTROL_handle_frame(NULL, &fr);
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_OIL_TEMP(void* ctx, uint16_t engine_oil_temp)
{
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_KICKDOWN(void* ctx)
{
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_VALVE_HEALTH(void* ctx, uint8_t valve0, uint8_t valve1, uint8_t valve2, uint8_t valve3, uint8_t valve4, uint8_t valve5, uint8_t valve6, uint8_t valve7)
{
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_SLEEP(void* ctx)
{
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_START(void* ctx)
{
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_CONSUMPTION(void* ctx, uint16_t ml_per_sec, uint16_t ml_per_km)
{
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_UPM(void* ctx, uint8_t upm, uint8_t level, uint8_t one)
{
    return 0;
}

int node_ECU_ENGINE_CONTROL_handle_ENGINE_STOP(void* ctx)
{
    return 0;
}
