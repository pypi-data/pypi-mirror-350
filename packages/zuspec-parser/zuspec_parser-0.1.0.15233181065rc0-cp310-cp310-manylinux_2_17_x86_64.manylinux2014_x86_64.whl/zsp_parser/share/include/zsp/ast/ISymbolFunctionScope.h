/****************************************************************************
 * ISymbolFunctionScope.h
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
class IFunctionPrototype;
using IFunctionPrototypeUP=UP<IFunctionPrototype>;
typedef std::shared_ptr<IFunctionPrototype> IFunctionPrototypeSP;
class IFunctionImport;
using IFunctionImportUP=UP<IFunctionImport>;
typedef std::shared_ptr<IFunctionImport> IFunctionImportSP;
class IFunctionDefinition;
using IFunctionDefinitionUP=UP<IFunctionDefinition>;
typedef std::shared_ptr<IFunctionDefinition> IFunctionDefinitionSP;
class IExecScope;
using IExecScopeUP=UP<IExecScope>;
typedef std::shared_ptr<IExecScope> IExecScopeSP;
class ISymbolFunctionScope;
using ISymbolFunctionScopeUP=UP<ISymbolFunctionScope>;
class ISymbolFunctionScope : public virtual ISymbolScope {
public:
    
    virtual ~ISymbolFunctionScope() { }
    
    
    virtual const std::vector<IFunctionPrototype *> &getPrototypes() const = 0;
    
    virtual std::vector<IFunctionPrototype *> &getPrototypes() = 0;
    
    virtual const std::vector<IFunctionImportUP> &getImport_specs() const = 0;
    
    virtual std::vector<IFunctionImportUP> &getImport_specs() = 0;
    
    virtual IFunctionDefinition *getDefinition() = 0;
    
    virtual void setDefinition(IFunctionDefinition *v) = 0;
    
    virtual ISymbolScope *getPlist() const = 0;
    
    virtual void setPlist(ISymbolScope *v, bool own=true) = 0;
    
    virtual IExecScope *getBody() = 0;
    
    virtual void setBody(IExecScope *v) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
