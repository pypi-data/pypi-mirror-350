/****************************************************************************
 * IActivitySelectBranch.h
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
namespace zsp {
namespace ast {

class IExpr;
using IExprUP=UP<IExpr>;
typedef std::shared_ptr<IExpr> IExprSP;
class IScopeChild;
using IScopeChildUP=UP<IScopeChild>;
typedef std::shared_ptr<IScopeChild> IScopeChildSP;
class IActivitySelectBranch;
using IActivitySelectBranchUP=UP<IActivitySelectBranch>;
class IActivitySelectBranch {
public:
    
    virtual ~IActivitySelectBranch() { }
    
    
    virtual IExpr *getGuard() const = 0;
    
    virtual void setGuard(IExpr *v, bool own=true) = 0;
    
    virtual IExpr *getWeight() const = 0;
    
    virtual void setWeight(IExpr *v, bool own=true) = 0;
    
    virtual IScopeChild *getBody() const = 0;
    
    virtual void setBody(IScopeChild *v, bool own=true) = 0;
    virtual void accept(IVisitor *v) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
