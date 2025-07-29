/****************************************************************************
 * IExtendType.h
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

#include "zsp/ast/ExtendTargetE.h"
namespace zsp {
namespace ast {

class IScope;
using IScopeUP=UP<IScope>;
typedef std::shared_ptr<IScope> IScopeSP;
class ITypeIdentifier;
using ITypeIdentifierUP=UP<ITypeIdentifier>;
typedef std::shared_ptr<ITypeIdentifier> ITypeIdentifierSP;
class ISymbolImportSpec;
using ISymbolImportSpecUP=UP<ISymbolImportSpec>;
typedef std::shared_ptr<ISymbolImportSpec> ISymbolImportSpecSP;
class IExtendType;
using IExtendTypeUP=UP<IExtendType>;
class IExtendType : public virtual IScope {
public:
    
    virtual ~IExtendType() { }
    
    
    virtual ExtendTargetE getKind() const = 0;
    
    virtual void setKind(ExtendTargetE v) = 0;
    
    virtual ITypeIdentifier *getTarget() const = 0;
    
    virtual void setTarget(ITypeIdentifier *v, bool own=true) = 0;
    
    virtual const std::unordered_map<std::string,int32_t> &getSymtab() const = 0;
    
    virtual std::unordered_map<std::string,int32_t> &getSymtab() = 0;
    
    virtual ISymbolImportSpec *getImports() const = 0;
    
    virtual void setImports(ISymbolImportSpec *v, bool own=true) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
