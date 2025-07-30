/****************************************************************************
 * IActivityActionTypeTraversal.h
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
#include "zsp/ast/IActivityLabeledStmt.h"

namespace zsp {
namespace ast {

class IActivityLabeledStmt;
using IActivityLabeledStmtUP=UP<IActivityLabeledStmt>;
typedef std::shared_ptr<IActivityLabeledStmt> IActivityLabeledStmtSP;
class IDataTypeUserDefined;
using IDataTypeUserDefinedUP=UP<IDataTypeUserDefined>;
typedef std::shared_ptr<IDataTypeUserDefined> IDataTypeUserDefinedSP;
class IConstraintStmt;
using IConstraintStmtUP=UP<IConstraintStmt>;
typedef std::shared_ptr<IConstraintStmt> IConstraintStmtSP;
class IActivityActionTypeTraversal;
using IActivityActionTypeTraversalUP=UP<IActivityActionTypeTraversal>;
class IActivityActionTypeTraversal : public virtual IActivityLabeledStmt {
public:
    
    virtual ~IActivityActionTypeTraversal() { }
    
    
    virtual IDataTypeUserDefined *getTarget() const = 0;
    
    virtual void setTarget(IDataTypeUserDefined *v, bool own=true) = 0;
    
    virtual IConstraintStmt *getWith_c() const = 0;
    
    virtual void setWith_c(IConstraintStmt *v, bool own=true) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
