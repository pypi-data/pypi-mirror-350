/****************************************************************************
 * IExprAggrMap.h
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
#include "zsp/ast/IExprAggrLiteral.h"

namespace zsp {
namespace ast {

class IExprAggrLiteral;
using IExprAggrLiteralUP=UP<IExprAggrLiteral>;
typedef std::shared_ptr<IExprAggrLiteral> IExprAggrLiteralSP;
class IExprAggrMapElem;
using IExprAggrMapElemUP=UP<IExprAggrMapElem>;
typedef std::shared_ptr<IExprAggrMapElem> IExprAggrMapElemSP;
class IExprAggrMap;
using IExprAggrMapUP=UP<IExprAggrMap>;
class IExprAggrMap : public virtual IExprAggrLiteral {
public:
    
    virtual ~IExprAggrMap() { }
    
    
    virtual const std::vector<IExprAggrMapElemUP> &getElems() const = 0;
    
    virtual std::vector<IExprAggrMapElemUP> &getElems() = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
