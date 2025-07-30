/****************************************************************************
 * FieldAttr.h
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 ****************************************************************************/
#pragma once
#include <stdint.h>

namespace zsp {
namespace ast {

enum class FieldAttr {
    NoFlags = 0,
    Action = (1 << 0),
    Builtin = (1 << 1),
    Rand = (1 << 2),
    Const = (1 << 3),
    Static = (1 << 4),
    Private = (1 << 5),
    Protected = (1 << 6)
};

static inline FieldAttr operator | (const FieldAttr lhs, const FieldAttr rhs) {
    return static_cast<FieldAttr>(static_cast<uint32_t>(lhs) | static_cast<uint32_t>(rhs));
}

static inline FieldAttr operator |= (FieldAttr &lhs, const FieldAttr rhs) {
    lhs = static_cast<FieldAttr>(static_cast<uint32_t>(lhs) | static_cast<uint32_t>(rhs));
    return lhs;
}

static inline FieldAttr operator & (const FieldAttr lhs, const FieldAttr rhs) {
    return static_cast<FieldAttr>(static_cast<uint32_t>(lhs) & static_cast<uint32_t>(rhs));
}

static inline FieldAttr operator ~ (const FieldAttr lhs) {
    return static_cast<FieldAttr>(~static_cast<uint32_t>(lhs));
}


} // namespace zsp
} // namespace ast

