/****************************************************************************
 * IRootSymbolScope.h
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
#include "zsp/ast/ISymbolScope.h"

namespace zsp {
namespace ast {

class ISymbolScope;
using ISymbolScopeUP=UP<ISymbolScope>;
typedef std::shared_ptr<ISymbolScope> ISymbolScopeSP;
class IGlobalScope;
using IGlobalScopeUP=UP<IGlobalScope>;
typedef std::shared_ptr<IGlobalScope> IGlobalScopeSP;
class IRootSymbolScope;
using IRootSymbolScopeUP=UP<IRootSymbolScope>;
class IRootSymbolScope : public virtual ISymbolScope {
public:
    
    virtual ~IRootSymbolScope() { }
    
    
    virtual const std::vector<IGlobalScopeUP> &getUnits() const = 0;
    
    virtual std::vector<IGlobalScopeUP> &getUnits() = 0;
    
    virtual const std::unordered_map<int32_t,std::string> &getFilenames() const = 0;
    
    virtual std::unordered_map<int32_t,std::string> &getFilenames() = 0;
    
    virtual const std::unordered_map<int32_t,int32_t> &getId2idx() const = 0;
    
    virtual std::unordered_map<int32_t,int32_t> &getId2idx() = 0;
    
    virtual const std::vector<std::vector<int32_t>> &getFileOutRef() const = 0;
    
    virtual std::vector<std::vector<int32_t>> &getFileOutRef() = 0;
    
    virtual const std::vector<std::vector<int32_t>> &getFileInRef() const = 0;
    
    virtual std::vector<std::vector<int32_t>> &getFileInRef() = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
