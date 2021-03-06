# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pr.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pr.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x08pr.proto\"(\n\ttopicData\x12\r\n\x05topic\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"2\n\x0etopicSubscribe\x12\r\n\x05topic\x18\x01 \x01(\t\x12\x11\n\tclient_ip\x18\x02 \x01(\t\"?\n\rtopicDataType\x12\r\n\x05topic\x18\x01 \x01(\t\x12\x11\n\tclient_ip\x18\x02 \x01(\t\x12\x0c\n\x04type\x18\x03 \x01(\t\"\x16\n\x05topic\x12\r\n\x05topic\x18\x01 \x01(\t\"\x11\n\x03ips\x12\n\n\x02ip\x18\x01 \x01(\t\"\x1a\n\x0b\x61\x63knowledge\x12\x0b\n\x03\x61\x63k\x18\x01 \x01(\t\"\x07\n\x05\x65mpty\"\x89\x01\n\x0f\x63ommit_req_data\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\r\n\x05level\x18\x02 \x01(\t\x12\x0e\n\x06\x64\x61ta_1\x18\x03 \x01(\t\x12\x0e\n\x06\x64\x61ta_2\x18\x04 \x01(\t\x12\x0e\n\x06\x64\x61ta_3\x18\x05 \x01(\t\x12\x10\n\x08\x66ilename\x18\x06 \x01(\t\x12\x15\n\rfunction_name\x18\x07 \x01(\t2\xb1\t\n\x0cPublishTopic\x12,\n\x0epublishRequest\x12\n.topicData\x1a\x0c.acknowledge\"\x00\x12\x33\n\x10subscribeRequest\x12\x0f.topicSubscribe\x1a\x0c.acknowledge\"\x00\x12\x39\n\x17subscribeRequestCentral\x12\x0e.topicDataType\x1a\x0c.acknowledge\"\x00\x12\x1b\n\x07giveIps\x12\x06.topic\x1a\x04.ips\"\x00\x30\x01\x12%\n\x07publish\x12\n.topicData\x1a\x0c.acknowledge\"\x00\x12\x1c\n\ngetFrontIp\x12\x06.empty\x1a\x04.ips\"\x00\x12\"\n\nregisterIp\x12\x04.ips\x1a\x0c.acknowledge\"\x00\x12\x34\n\x11sendBackupRequest\x12\x0f.topicSubscribe\x1a\x0c.acknowledge\"\x00\x12*\n\nsendBackup\x12\n.topicData\x1a\x0c.acknowledge\"\x00(\x01\x12-\n\rforwardBackup\x12\n.topicData\x1a\x0c.acknowledge\"\x00(\x01\x12.\n\x11giveSubscriberIps\x12\x0f.topicSubscribe\x1a\x04.ips\"\x00\x30\x01\x12&\n\x08sendData\x12\n.topicData\x1a\x0c.acknowledge\"\x00\x12\x31\n\x0ereplicaRequest\x12\x0f.topicSubscribe\x1a\x0c.acknowledge\"\x00\x12\"\n\x0cquerryTopics\x12\x06.empty\x1a\x06.topic\"\x00\x30\x01\x12;\n\x18sendBackupRequestReplica\x12\x0f.topicSubscribe\x1a\x0c.acknowledge\"\x00\x12\x31\n\x11sendBackupReplica\x12\n.topicData\x1a\x0c.acknowledge\"\x00(\x01\x12\x37\n\x12unsubscribeRequest\x12\x0f.topicSubscribe\x1a\x0c.acknowledge\"\x00(\x01\x12\x33\n\x10\x64\x65ReplicaRequest\x12\x0f.topicSubscribe\x1a\x0c.acknowledge\"\x00\x12<\n\x19unsubscribeRequestCentral\x12\x0f.topicSubscribe\x1a\x0c.acknowledge\"\x00\x12\x32\n\x0e\x63ommit_request\x12\x10.commit_req_data\x1a\x0c.acknowledge\"\x00\x12\x34\n\x10\x63ommit_phase_two\x12\x10.commit_req_data\x1a\x0c.acknowledge\"\x00\x12\'\n\rupgradeBackup\x12\x06.empty\x1a\x0c.acknowledge\"\x00\x12$\n\x10giveDataPhaseOne\x12\x06.empty\x1a\x06.topic\"\x00\x12*\n\x10giveDataPhaseTwo\x12\x06.empty\x1a\x0c.acknowledge\"\x00\x12\x1d\n\x0bgetMasterIp\x12\x06.empty\x1a\x04.ips\"\x00\x12\x1d\n\x0bgetBackupIp\x12\x06.empty\x1a\x04.ips\"\x00\x62\x06proto3')
)




_TOPICDATA = _descriptor.Descriptor(
  name='topicData',
  full_name='topicData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='topic', full_name='topicData.topic', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='topicData.data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=12,
  serialized_end=52,
)


_TOPICSUBSCRIBE = _descriptor.Descriptor(
  name='topicSubscribe',
  full_name='topicSubscribe',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='topic', full_name='topicSubscribe.topic', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_ip', full_name='topicSubscribe.client_ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=54,
  serialized_end=104,
)


_TOPICDATATYPE = _descriptor.Descriptor(
  name='topicDataType',
  full_name='topicDataType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='topic', full_name='topicDataType.topic', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_ip', full_name='topicDataType.client_ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='topicDataType.type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=169,
)


_TOPIC = _descriptor.Descriptor(
  name='topic',
  full_name='topic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='topic', full_name='topic.topic', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=193,
)


_IPS = _descriptor.Descriptor(
  name='ips',
  full_name='ips',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='ips.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=195,
  serialized_end=212,
)


_ACKNOWLEDGE = _descriptor.Descriptor(
  name='acknowledge',
  full_name='acknowledge',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ack', full_name='acknowledge.ack', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=214,
  serialized_end=240,
)


_EMPTY = _descriptor.Descriptor(
  name='empty',
  full_name='empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=242,
  serialized_end=249,
)


_COMMIT_REQ_DATA = _descriptor.Descriptor(
  name='commit_req_data',
  full_name='commit_req_data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='commit_req_data.action', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='level', full_name='commit_req_data.level', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data_1', full_name='commit_req_data.data_1', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data_2', full_name='commit_req_data.data_2', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data_3', full_name='commit_req_data.data_3', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filename', full_name='commit_req_data.filename', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='function_name', full_name='commit_req_data.function_name', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=252,
  serialized_end=389,
)

DESCRIPTOR.message_types_by_name['topicData'] = _TOPICDATA
DESCRIPTOR.message_types_by_name['topicSubscribe'] = _TOPICSUBSCRIBE
DESCRIPTOR.message_types_by_name['topicDataType'] = _TOPICDATATYPE
DESCRIPTOR.message_types_by_name['topic'] = _TOPIC
DESCRIPTOR.message_types_by_name['ips'] = _IPS
DESCRIPTOR.message_types_by_name['acknowledge'] = _ACKNOWLEDGE
DESCRIPTOR.message_types_by_name['empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['commit_req_data'] = _COMMIT_REQ_DATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

topicData = _reflection.GeneratedProtocolMessageType('topicData', (_message.Message,), dict(
  DESCRIPTOR = _TOPICDATA,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:topicData)
  ))
_sym_db.RegisterMessage(topicData)

topicSubscribe = _reflection.GeneratedProtocolMessageType('topicSubscribe', (_message.Message,), dict(
  DESCRIPTOR = _TOPICSUBSCRIBE,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:topicSubscribe)
  ))
_sym_db.RegisterMessage(topicSubscribe)

topicDataType = _reflection.GeneratedProtocolMessageType('topicDataType', (_message.Message,), dict(
  DESCRIPTOR = _TOPICDATATYPE,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:topicDataType)
  ))
_sym_db.RegisterMessage(topicDataType)

topic = _reflection.GeneratedProtocolMessageType('topic', (_message.Message,), dict(
  DESCRIPTOR = _TOPIC,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:topic)
  ))
_sym_db.RegisterMessage(topic)

ips = _reflection.GeneratedProtocolMessageType('ips', (_message.Message,), dict(
  DESCRIPTOR = _IPS,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:ips)
  ))
_sym_db.RegisterMessage(ips)

acknowledge = _reflection.GeneratedProtocolMessageType('acknowledge', (_message.Message,), dict(
  DESCRIPTOR = _ACKNOWLEDGE,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:acknowledge)
  ))
_sym_db.RegisterMessage(acknowledge)

empty = _reflection.GeneratedProtocolMessageType('empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:empty)
  ))
_sym_db.RegisterMessage(empty)

commit_req_data = _reflection.GeneratedProtocolMessageType('commit_req_data', (_message.Message,), dict(
  DESCRIPTOR = _COMMIT_REQ_DATA,
  __module__ = 'pr_pb2'
  # @@protoc_insertion_point(class_scope:commit_req_data)
  ))
_sym_db.RegisterMessage(commit_req_data)



_PUBLISHTOPIC = _descriptor.ServiceDescriptor(
  name='PublishTopic',
  full_name='PublishTopic',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=392,
  serialized_end=1593,
  methods=[
  _descriptor.MethodDescriptor(
    name='publishRequest',
    full_name='PublishTopic.publishRequest',
    index=0,
    containing_service=None,
    input_type=_TOPICDATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='subscribeRequest',
    full_name='PublishTopic.subscribeRequest',
    index=1,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='subscribeRequestCentral',
    full_name='PublishTopic.subscribeRequestCentral',
    index=2,
    containing_service=None,
    input_type=_TOPICDATATYPE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='giveIps',
    full_name='PublishTopic.giveIps',
    index=3,
    containing_service=None,
    input_type=_TOPIC,
    output_type=_IPS,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='publish',
    full_name='PublishTopic.publish',
    index=4,
    containing_service=None,
    input_type=_TOPICDATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getFrontIp',
    full_name='PublishTopic.getFrontIp',
    index=5,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_IPS,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='registerIp',
    full_name='PublishTopic.registerIp',
    index=6,
    containing_service=None,
    input_type=_IPS,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='sendBackupRequest',
    full_name='PublishTopic.sendBackupRequest',
    index=7,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='sendBackup',
    full_name='PublishTopic.sendBackup',
    index=8,
    containing_service=None,
    input_type=_TOPICDATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='forwardBackup',
    full_name='PublishTopic.forwardBackup',
    index=9,
    containing_service=None,
    input_type=_TOPICDATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='giveSubscriberIps',
    full_name='PublishTopic.giveSubscriberIps',
    index=10,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_IPS,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='sendData',
    full_name='PublishTopic.sendData',
    index=11,
    containing_service=None,
    input_type=_TOPICDATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='replicaRequest',
    full_name='PublishTopic.replicaRequest',
    index=12,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='querryTopics',
    full_name='PublishTopic.querryTopics',
    index=13,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_TOPIC,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='sendBackupRequestReplica',
    full_name='PublishTopic.sendBackupRequestReplica',
    index=14,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='sendBackupReplica',
    full_name='PublishTopic.sendBackupReplica',
    index=15,
    containing_service=None,
    input_type=_TOPICDATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='unsubscribeRequest',
    full_name='PublishTopic.unsubscribeRequest',
    index=16,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='deReplicaRequest',
    full_name='PublishTopic.deReplicaRequest',
    index=17,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='unsubscribeRequestCentral',
    full_name='PublishTopic.unsubscribeRequestCentral',
    index=18,
    containing_service=None,
    input_type=_TOPICSUBSCRIBE,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='commit_request',
    full_name='PublishTopic.commit_request',
    index=19,
    containing_service=None,
    input_type=_COMMIT_REQ_DATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='commit_phase_two',
    full_name='PublishTopic.commit_phase_two',
    index=20,
    containing_service=None,
    input_type=_COMMIT_REQ_DATA,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='upgradeBackup',
    full_name='PublishTopic.upgradeBackup',
    index=21,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='giveDataPhaseOne',
    full_name='PublishTopic.giveDataPhaseOne',
    index=22,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_TOPIC,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='giveDataPhaseTwo',
    full_name='PublishTopic.giveDataPhaseTwo',
    index=23,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_ACKNOWLEDGE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getMasterIp',
    full_name='PublishTopic.getMasterIp',
    index=24,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_IPS,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getBackupIp',
    full_name='PublishTopic.getBackupIp',
    index=25,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_IPS,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PUBLISHTOPIC)

DESCRIPTOR.services_by_name['PublishTopic'] = _PUBLISHTOPIC

# @@protoc_insertion_point(module_scope)
