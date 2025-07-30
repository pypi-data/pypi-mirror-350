/****************************************************************************
 * UP.h
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

namespace zsp {
namespace ast {

template <class T> struct UPD {
    UPD() : m_owned(true) { }
    UPD(bool &owned) : m_owned(owned) { }
    void operator()(T *p) {
        if (p && m_owned) {
            delete p;
        }
    }
    bool m_owned;
};

template <class T> class UP : public std::unique_ptr<T,UPD<T>> {
public:
    UP() : std::unique_ptr<T,UPD<T>>() {}
    UP(T *p, bool owned=true) : std::unique_ptr<T,UPD<T>>(p, UPD<T>(owned)) {}
    bool owned() const { return std::unique_ptr<T,UPD<T>>::get_deleter().m_owned; }
};

} // namespace zsp
} // namespace ast

