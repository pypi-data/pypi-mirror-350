#!/bin/bash

set -e

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
autonomous_proto_dir=${SCRIPT_DIR}/..
proto_files_dir=${autonomous_proto_dir}/proto
output_dir=${SCRIPT_DIR}/src/autonomous_proto

python -m grpc_tools.protoc -I ${output_dir} --proto_path=${proto_files_dir} --python_betterproto_out=${output_dir} ${proto_files_dir}/*.proto

#rm -rf ./*.py
#python -m grpc_tools.protoc -I . --proto_path=../../proto --python_betterproto_out=. ../../proto/*.proto