#pragma once


/* This is an autogenerated hpp file, please don't modify directly. Instead modify the helper.template file in Inc 
 * and regenerate the helpers by running the gen_helpers.py script in Tools.
 * Thanks
 */

#include "JetsonLandingInitiationCommand.hpp"
#include "CRC32.hpp"

namespace helpers
{

bool encodeJetsonLandingInitiationCommand(TelemMessages::JetsonLandingInitiationCommand msg, uint8_t* buf, int maxSize) {

    int size = sizeof(TelemMessages::JetsonLandingInitiationCommand);

    // check to make sure the size of the buffer is enough
    if(size > maxSize) return false;

    // fill in header values
    msg.header.flag = START_FLAG;
    msg.header.length[0] = 0;
    msg.header.length[1] = 1;
    msg.header.type = 3;

    // encode message
    msg._encodeNoHash(buf,0,size);

    // calculate checksum
    // the 7 is the number of bytes not included in the checksum (the flag, the length, and the checksum itself)
    uint32_t checksum = calculateChecksum(buf, size - 4);
    // checksum will be in little endian
    int endOfMessage = size - 1;
    buf[endOfMessage] = (checksum & 0xFF000000) >> 24; 
    buf[endOfMessage - 1] = (checksum & 0x00FF0000) >> 16; 
    buf[endOfMessage - 2] = (checksum & 0x0000FF00) >> 8; 
    buf[endOfMessage - 3] = checksum & 0x000000FF; 

    return true;
}

TelemMessages::JetsonLandingInitiationCommand decodeJetsonLandingInitiationCommand(uint8_t* buf, int maxSize) {

    int size = sizeof(TelemMessages::JetsonLandingInitiationCommand);
    TelemMessages::JetsonLandingInitiationCommand msg;

    // check to make sure the size of the buffer is enough, just in case
    if(size > maxSize) {
        msg.header.flag = 0;
        return msg;
    } 

    // encode message
    msg._decodeNoHash(buf,0,maxSize);

    // calculate checksum
    // the 7 is the number of bytes not included in the checksum (the flag, the length, and the checksum itself)
    uint32_t checksum = calculateChecksum(buf, size - 4);
    // checksum will be in little endian
    int endOfMessage = size - 1;
    uint32_t checksumFromMessage = buf[endOfMessage - 3] << 24;
    checksumFromMessage = checksumFromMessage | (buf[endOfMessage - 2] << 16);
    checksumFromMessage = checksumFromMessage | (buf[endOfMessage - 1] << 8);
    checksumFromMessage = checksumFromMessage | buf[endOfMessage];

    if(checksum != checksumFromMessage) {
        msg.header.flag = 0;
        return msg;
    }
    return msg;
}

}