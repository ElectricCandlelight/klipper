// Hello world command implementation
//
// Copyright (C) 2024 <Your Name>
// This file may be distributed under the terms of the GNU GPLv3 license.

#include "command.h" // For DECL_COMMAND_FLAGS
#include "sched.h"   // For sched_read_time()

void
command_hello_response(uint32_t *args)
{
    uint8_t oid = args[0];
    sendf("hello_response oid=%c value=%s", oid, "A0");
}
DECL_COMMAND(command_hello_response, "hello_response oid=%c");