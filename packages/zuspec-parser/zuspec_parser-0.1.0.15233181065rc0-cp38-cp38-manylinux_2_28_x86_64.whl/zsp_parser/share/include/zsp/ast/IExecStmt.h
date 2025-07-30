/****************************************************************************
 * IExecStmt.h
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
#include "zsp/ast/IScopeChild.h"

namespace zsp {
namespace ast {

class IScopeChild;
using IScopeChildUP=UP<IScopeChild>;
typedef std::shared_ptr<IScopeChild> IScopeChildSP;
class ISymbolScope;
using ISymbolScopeUP=UP<ISymbolScope>;
typedef std::shared_ptr<ISymbolScope> ISymbolScopeSP;
class IExecStmt;
using IExecStmtUP=UP<IExecStmt>;
class IExecStmt : public virtual IScopeChild {
public:
    
    virtual ~IExecStmt() { }
    
    
    virtual ISymbolScope *getUpper() = 0;
    
    virtual void setUpper(ISymbolScope *v) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
