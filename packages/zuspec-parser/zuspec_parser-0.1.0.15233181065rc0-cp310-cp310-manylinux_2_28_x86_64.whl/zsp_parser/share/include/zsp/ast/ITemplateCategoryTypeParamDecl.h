/****************************************************************************
 * ITemplateCategoryTypeParamDecl.h
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
#include "zsp/ast/ITemplateParamDecl.h"

#include "zsp/ast/TypeCategory.h"
namespace zsp {
namespace ast {

class ITemplateParamDecl;
using ITemplateParamDeclUP=UP<ITemplateParamDecl>;
typedef std::shared_ptr<ITemplateParamDecl> ITemplateParamDeclSP;
class ITypeIdentifier;
using ITypeIdentifierUP=UP<ITypeIdentifier>;
typedef std::shared_ptr<ITypeIdentifier> ITypeIdentifierSP;
class IDataType;
using IDataTypeUP=UP<IDataType>;
typedef std::shared_ptr<IDataType> IDataTypeSP;
class ITemplateCategoryTypeParamDecl;
using ITemplateCategoryTypeParamDeclUP=UP<ITemplateCategoryTypeParamDecl>;
class ITemplateCategoryTypeParamDecl : public virtual ITemplateParamDecl {
public:
    
    virtual ~ITemplateCategoryTypeParamDecl() { }
    
    
    virtual TypeCategory getCategory() const = 0;
    
    virtual void setCategory(TypeCategory v) = 0;
    
    virtual ITypeIdentifier *getRestriction() const = 0;
    
    virtual void setRestriction(ITypeIdentifier *v, bool own=true) = 0;
    
    virtual IDataType *getDflt() const = 0;
    
    virtual void setDflt(IDataType *v, bool own=true) = 0;
};
    
    } // namespace zsp
    } // namespace ast
    
