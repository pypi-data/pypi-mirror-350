/****************************************************************************
 * IGlobalScope.h
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
#include <unordered_map>
#include <memory>
#include <set>
#include <string>
#include <vector>
#include "zsp/ast/impl/UP.h"
#include "zsp/ast/IVisitor.h"
#include "zsp/ast/IScope.h"

namespace zsp {
namespace ast {

class IScope;
using IScopeUP=UP<IScope>;
typedef std::shared_ptr<IScope> IScopeSP;
class IGlobalScope;
using IGlobalScopeUP=UP<IGlobalScope>;
class IGlobalScope : public virtual IScope {
public:
    
    virtual ~IGlobalScope() { }
    
    
    virtual int32_t getFileid() const = 0;
    
    virtual void setFileid(int32_t v) = 0;
    
    virtual const std::string &getFilename() const = 0;
    
    virtual void setFilename(const std::string &v) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
