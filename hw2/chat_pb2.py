# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\":\n\x07Message\x12\x13\n\x0broom_number\x18\x01 \x01(\x05\x12\x0c\n\x04user\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\"0\n\x0bJoinRequest\x12\x13\n\x0broom_number\x18\x01 \x01(\x05\x12\x0c\n\x04user\x18\x02 \x01(\t\"!\n\nRoomNumber\x12\x13\n\x0broom_number\x18\x01 \x01(\x05\"\x1f\n\nRoomStatus\x12\x11\n\tis_filled\x18\x01 \x01(\x08\"1\n\x08Username\x12\x13\n\x0broom_number\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\"\"\n\x0eUsernameStatus\x12\x10\n\x08is_taken\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty\"0\n\x0bQuitRequest\x12\x13\n\x0broom_number\x18\x01 \x01(\x05\x12\x0c\n\x04user\x18\x02 \x01(\t\"\x18\n\x08UserList\x12\x0c\n\x04user\x18\x01 \x03(\t2\xb9\x02\n\x04\x43hat\x12+\n\x0bSendMessage\x12\r.chat.Message\x1a\x0b.chat.Empty\"\x00\x12\x37\n\x0fReceiveMessages\x12\x11.chat.JoinRequest\x1a\r.chat.Message\"\x00\x30\x01\x12\x31\n\tCheckRoom\x12\x10.chat.RoomNumber\x1a\x10.chat.RoomStatus\"\x00\x12\x37\n\rCheckUsername\x12\x0e.chat.Username\x1a\x14.chat.UsernameStatus\"\x00\x12(\n\x04Quit\x12\x11.chat.QuitRequest\x1a\x0b.chat.Empty\"\x00\x12\x35\n\x0fListActiveUsers\x12\x10.chat.RoomNumber\x1a\x0e.chat.UserList\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=20
  _MESSAGE._serialized_end=78
  _JOINREQUEST._serialized_start=80
  _JOINREQUEST._serialized_end=128
  _ROOMNUMBER._serialized_start=130
  _ROOMNUMBER._serialized_end=163
  _ROOMSTATUS._serialized_start=165
  _ROOMSTATUS._serialized_end=196
  _USERNAME._serialized_start=198
  _USERNAME._serialized_end=247
  _USERNAMESTATUS._serialized_start=249
  _USERNAMESTATUS._serialized_end=283
  _EMPTY._serialized_start=285
  _EMPTY._serialized_end=292
  _QUITREQUEST._serialized_start=294
  _QUITREQUEST._serialized_end=342
  _USERLIST._serialized_start=344
  _USERLIST._serialized_end=368
  _CHAT._serialized_start=371
  _CHAT._serialized_end=684
# @@protoc_insertion_point(module_scope)
