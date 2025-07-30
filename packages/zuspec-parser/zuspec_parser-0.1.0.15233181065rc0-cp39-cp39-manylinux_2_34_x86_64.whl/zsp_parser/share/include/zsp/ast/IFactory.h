/****************************************************************************
 * IFactory.h
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

#include <memory>
#include "zsp/ast/AssignOp.h"
#include "zsp/ast/ExecKind.h"
#include "zsp/ast/ExprBinOp.h"
#include "zsp/ast/ExprUnaryOp.h"
#include "zsp/ast/ExtendTargetE.h"
#include "zsp/ast/FunctionParamDeclKind.h"
#include "zsp/ast/ParamDir.h"
#include "zsp/ast/PlatQual.h"
#include "zsp/ast/StructKind.h"
#include "zsp/ast/SymbolRefPathElemKind.h"
#include "zsp/ast/TypeCategory.h"
#include "zsp/ast/IExprAggrMapElem.h"
#include "zsp/ast/ITemplateParamDeclList.h"
#include "zsp/ast/IExprAggrStructElem.h"
#include "zsp/ast/ITemplateParamValue.h"
#include "zsp/ast/ITemplateParamValueList.h"
#include "zsp/ast/IActivityJoinSpec.h"
#include "zsp/ast/IRefExpr.h"
#include "zsp/ast/IActivityMatchChoice.h"
#include "zsp/ast/IScopeChild.h"
#include "zsp/ast/IActivitySelectBranch.h"
#include "zsp/ast/ISymbolRefPath.h"
#include "zsp/ast/IExecTargetTemplateParam.h"
#include "zsp/ast/IExpr.h"
#include "zsp/ast/IAssocData.h"
#include "zsp/ast/ISymbolImportSpec.h"
#include "zsp/ast/IPyImportFromStmt.h"
#include "zsp/ast/IActivityJoinSpecBranch.h"
#include "zsp/ast/IActivityJoinSpecFirst.h"
#include "zsp/ast/IActivityJoinSpecNone.h"
#include "zsp/ast/IActivityJoinSpecSelect.h"
#include "zsp/ast/IPyImportStmt.h"
#include "zsp/ast/IRefExprScopeIndex.h"
#include "zsp/ast/IRefExprTypeScopeContext.h"
#include "zsp/ast/IRefExprTypeScopeGlobal.h"
#include "zsp/ast/IScope.h"
#include "zsp/ast/IScopeChildRef.h"
#include "zsp/ast/ISymbolChild.h"
#include "zsp/ast/IActivitySchedulingConstraint.h"
#include "zsp/ast/IActivityStmt.h"
#include "zsp/ast/ISymbolScopeRef.h"
#include "zsp/ast/ITemplateParamDecl.h"
#include "zsp/ast/IConstraintStmt.h"
#include "zsp/ast/ITemplateParamExprValue.h"
#include "zsp/ast/ITemplateParamTypeValue.h"
#include "zsp/ast/ITypeIdentifier.h"
#include "zsp/ast/ITypeIdentifierElem.h"
#include "zsp/ast/IDataType.h"
#include "zsp/ast/IExecStmt.h"
#include "zsp/ast/IExecTargetTemplateBlock.h"
#include "zsp/ast/IExprAggrLiteral.h"
#include "zsp/ast/IExprBin.h"
#include "zsp/ast/IExprBitSlice.h"
#include "zsp/ast/IExprBool.h"
#include "zsp/ast/IExprCast.h"
#include "zsp/ast/IExprCompileHas.h"
#include "zsp/ast/IExprCond.h"
#include "zsp/ast/IExprDomainOpenRangeList.h"
#include "zsp/ast/IExprDomainOpenRangeValue.h"
#include "zsp/ast/IExprHierarchicalId.h"
#include "zsp/ast/IExprId.h"
#include "zsp/ast/IExprIn.h"
#include "zsp/ast/IExprListLiteral.h"
#include "zsp/ast/IExprMemberPathElem.h"
#include "zsp/ast/IExprNull.h"
#include "zsp/ast/IExprNumber.h"
#include "zsp/ast/IExprOpenRangeList.h"
#include "zsp/ast/IExprOpenRangeValue.h"
#include "zsp/ast/IExprRefPath.h"
#include "zsp/ast/IExprRefPathElem.h"
#include "zsp/ast/IExprStaticRefPath.h"
#include "zsp/ast/IExprString.h"
#include "zsp/ast/IExprStructLiteral.h"
#include "zsp/ast/IExprStructLiteralItem.h"
#include "zsp/ast/IExprSubscript.h"
#include "zsp/ast/IExprUnary.h"
#include "zsp/ast/IExtendEnum.h"
#include "zsp/ast/IFunctionDefinition.h"
#include "zsp/ast/IFunctionImport.h"
#include "zsp/ast/IFunctionParamDecl.h"
#include "zsp/ast/IMethodParameterList.h"
#include "zsp/ast/INamedScopeChild.h"
#include "zsp/ast/IPackageImportStmt.h"
#include "zsp/ast/IProceduralStmtIfClause.h"
#include "zsp/ast/IProceduralStmtMatch.h"
#include "zsp/ast/IProceduralStmtMatchChoice.h"
#include "zsp/ast/IActivityBindStmt.h"
#include "zsp/ast/IActivityConstraint.h"
#include "zsp/ast/IProceduralStmtReturn.h"
#include "zsp/ast/IProceduralStmtYield.h"
#include "zsp/ast/IActivityLabeledStmt.h"
#include "zsp/ast/ISymbolChildrenScope.h"
#include "zsp/ast/ITemplateCategoryTypeParamDecl.h"
#include "zsp/ast/ITemplateGenericTypeParamDecl.h"
#include "zsp/ast/IConstraintScope.h"
#include "zsp/ast/IConstraintStmtDefault.h"
#include "zsp/ast/IConstraintStmtDefaultDisable.h"
#include "zsp/ast/IConstraintStmtExpr.h"
#include "zsp/ast/IConstraintStmtField.h"
#include "zsp/ast/ITemplateValueParamDecl.h"
#include "zsp/ast/IConstraintStmtIf.h"
#include "zsp/ast/IConstraintStmtUnique.h"
#include "zsp/ast/IDataTypeBool.h"
#include "zsp/ast/IDataTypeChandle.h"
#include "zsp/ast/IDataTypeEnum.h"
#include "zsp/ast/IDataTypeInt.h"
#include "zsp/ast/IDataTypePyObj.h"
#include "zsp/ast/IDataTypeRef.h"
#include "zsp/ast/IDataTypeString.h"
#include "zsp/ast/IDataTypeUserDefined.h"
#include "zsp/ast/IEnumDecl.h"
#include "zsp/ast/IEnumItem.h"
#include "zsp/ast/IExprAggrEmpty.h"
#include "zsp/ast/IExprAggrList.h"
#include "zsp/ast/IExprAggrMap.h"
#include "zsp/ast/IExprAggrStruct.h"
#include "zsp/ast/IExprRefPathContext.h"
#include "zsp/ast/IExprRefPathId.h"
#include "zsp/ast/IExprRefPathStatic.h"
#include "zsp/ast/IExprRefPathStaticRooted.h"
#include "zsp/ast/IExprSignedNumber.h"
#include "zsp/ast/IExprUnsignedNumber.h"
#include "zsp/ast/IExtendType.h"
#include "zsp/ast/IField.h"
#include "zsp/ast/IFieldClaim.h"
#include "zsp/ast/IFieldCompRef.h"
#include "zsp/ast/IFieldRef.h"
#include "zsp/ast/IFunctionImportProto.h"
#include "zsp/ast/IFunctionImportType.h"
#include "zsp/ast/IFunctionPrototype.h"
#include "zsp/ast/IGlobalScope.h"
#include "zsp/ast/INamedScope.h"
#include "zsp/ast/IPackageScope.h"
#include "zsp/ast/IProceduralStmtAssignment.h"
#include "zsp/ast/IProceduralStmtBody.h"
#include "zsp/ast/IProceduralStmtBreak.h"
#include "zsp/ast/IProceduralStmtContinue.h"
#include "zsp/ast/IProceduralStmtDataDeclaration.h"
#include "zsp/ast/IProceduralStmtExpr.h"
#include "zsp/ast/IProceduralStmtFunctionCall.h"
#include "zsp/ast/IProceduralStmtIfElse.h"
#include "zsp/ast/IActivityActionHandleTraversal.h"
#include "zsp/ast/IActivityActionTypeTraversal.h"
#include "zsp/ast/IProceduralStmtRepeatWhile.h"
#include "zsp/ast/IActivityForeach.h"
#include "zsp/ast/IActivityIfElse.h"
#include "zsp/ast/IProceduralStmtWhile.h"
#include "zsp/ast/IActivityMatch.h"
#include "zsp/ast/IActivityRepeatCount.h"
#include "zsp/ast/IActivityRepeatWhile.h"
#include "zsp/ast/IActivityReplicate.h"
#include "zsp/ast/IActivitySelect.h"
#include "zsp/ast/ISymbolScope.h"
#include "zsp/ast/IActivitySuper.h"
#include "zsp/ast/IConstraintBlock.h"
#include "zsp/ast/IConstraintStmtForall.h"
#include "zsp/ast/IConstraintStmtForeach.h"
#include "zsp/ast/IConstraintStmtImplication.h"
#include "zsp/ast/ITypeScope.h"
#include "zsp/ast/IExprRefPathStaticFunc.h"
#include "zsp/ast/IExprRefPathSuper.h"
#include "zsp/ast/IAction.h"
#include "zsp/ast/IActivityDecl.h"
#include "zsp/ast/IProceduralStmtSymbolBodyScope.h"
#include "zsp/ast/IConstraintSymbolScope.h"
#include "zsp/ast/IActivityLabeledScope.h"
#include "zsp/ast/IRootSymbolScope.h"
#include "zsp/ast/IStruct.h"
#include "zsp/ast/ISymbolEnumScope.h"
#include "zsp/ast/ISymbolExtendScope.h"
#include "zsp/ast/IExecScope.h"
#include "zsp/ast/ISymbolFunctionScope.h"
#include "zsp/ast/ISymbolTypeScope.h"
#include "zsp/ast/IComponent.h"
#include "zsp/ast/IProceduralStmtRepeat.h"
#include "zsp/ast/IActivityParallel.h"
#include "zsp/ast/IActivitySchedule.h"
#include "zsp/ast/IExecBlock.h"
#include "zsp/ast/IActivitySequence.h"
#include "zsp/ast/IProceduralStmtForeach.h"
namespace zsp {
namespace ast {

class IFactory;
using IFactoryUP=std::unique_ptr<IFactory>;
class IFactory {
public:

    virtual ~IFactory() { }
    
    virtual IExprAggrMapElem *mkExprAggrMapElem(    IExpr* lhs,
    IExpr* rhs) = 0;
    virtual ITemplateParamDeclList *mkTemplateParamDeclList() = 0;
    virtual IExprAggrStructElem *mkExprAggrStructElem(    IExprId* name,
    IExpr* value) = 0;
    virtual ITemplateParamValue *mkTemplateParamValue() = 0;
    virtual ITemplateParamValueList *mkTemplateParamValueList() = 0;
    virtual IActivityJoinSpec *mkActivityJoinSpec() = 0;
    virtual IRefExpr *mkRefExpr() = 0;
    virtual IActivityMatchChoice *mkActivityMatchChoice(    bool is_default,
    IExprOpenRangeList* cond,
    IScopeChild* body) = 0;
    virtual IScopeChild *mkScopeChild() = 0;
    virtual IActivitySelectBranch *mkActivitySelectBranch(    IExpr* guard,
    IExpr* weight,
    IScopeChild* body) = 0;
    virtual ISymbolRefPath *mkSymbolRefPath() = 0;
    virtual IExecTargetTemplateParam *mkExecTargetTemplateParam(    IExpr* expr,
    int32_t start,
    int32_t end) = 0;
    virtual IExpr *mkExpr() = 0;
    virtual IAssocData *mkAssocData() = 0;
    virtual ISymbolImportSpec *mkSymbolImportSpec() = 0;
    virtual IPyImportFromStmt *mkPyImportFromStmt() = 0;
    virtual IActivityJoinSpecBranch *mkActivityJoinSpecBranch() = 0;
    virtual IActivityJoinSpecFirst *mkActivityJoinSpecFirst(    IExpr* count) = 0;
    virtual IActivityJoinSpecNone *mkActivityJoinSpecNone() = 0;
    virtual IActivityJoinSpecSelect *mkActivityJoinSpecSelect(    IExpr* count) = 0;
    virtual IPyImportStmt *mkPyImportStmt() = 0;
    virtual IRefExprScopeIndex *mkRefExprScopeIndex(    IRefExpr* base,
    int32_t offset) = 0;
    virtual IRefExprTypeScopeContext *mkRefExprTypeScopeContext(    IRefExpr* base,
    int32_t offset) = 0;
    virtual IRefExprTypeScopeGlobal *mkRefExprTypeScopeGlobal(    int32_t fileid) = 0;
    virtual IScope *mkScope() = 0;
    virtual IScopeChildRef *mkScopeChildRef(    IScopeChild * target) = 0;
    virtual ISymbolChild *mkSymbolChild() = 0;
    virtual IActivitySchedulingConstraint *mkActivitySchedulingConstraint(    bool is_parallel) = 0;
    virtual IActivityStmt *mkActivityStmt() = 0;
    virtual ISymbolScopeRef *mkSymbolScopeRef(    std::string name) = 0;
    virtual ITemplateParamDecl *mkTemplateParamDecl(    IExprId* name) = 0;
    virtual IConstraintStmt *mkConstraintStmt() = 0;
    virtual ITemplateParamExprValue *mkTemplateParamExprValue(    IExpr* value) = 0;
    virtual ITemplateParamTypeValue *mkTemplateParamTypeValue(    IDataType* value) = 0;
    virtual ITypeIdentifier *mkTypeIdentifier() = 0;
    virtual ITypeIdentifierElem *mkTypeIdentifierElem(    IExprId* id,
    ITemplateParamValueList* params) = 0;
    virtual IDataType *mkDataType() = 0;
    virtual IExecStmt *mkExecStmt() = 0;
    virtual IExecTargetTemplateBlock *mkExecTargetTemplateBlock(    ExecKind kind,
    std::string data) = 0;
    virtual IExprAggrLiteral *mkExprAggrLiteral() = 0;
    virtual IExprBin *mkExprBin(    IExpr* lhs,
    ExprBinOp op,
    IExpr* rhs) = 0;
    virtual IExprBitSlice *mkExprBitSlice(    IExpr* lhs,
    IExpr* rhs) = 0;
    virtual IExprBool *mkExprBool(    bool value) = 0;
    virtual IExprCast *mkExprCast(    IDataType* casting_type,
    IExpr* expr) = 0;
    virtual IExprCompileHas *mkExprCompileHas(    IExprRefPathStatic* ref) = 0;
    virtual IExprCond *mkExprCond(    IExpr* cond_e,
    IExpr* true_e,
    IExpr* false_e) = 0;
    virtual IExprDomainOpenRangeList *mkExprDomainOpenRangeList() = 0;
    virtual IExprDomainOpenRangeValue *mkExprDomainOpenRangeValue(    bool single,
    IExpr* lhs,
    IExpr* rhs) = 0;
    virtual IExprHierarchicalId *mkExprHierarchicalId() = 0;
    virtual IExprId *mkExprId(    std::string id,
    bool is_escaped) = 0;
    virtual IExprIn *mkExprIn(    IExpr* lhs,
    IExprOpenRangeList* rhs) = 0;
    virtual IExprListLiteral *mkExprListLiteral() = 0;
    virtual IExprMemberPathElem *mkExprMemberPathElem(    IExprId* id,
    IMethodParameterList* params) = 0;
    virtual IExprNull *mkExprNull() = 0;
    virtual IExprNumber *mkExprNumber() = 0;
    virtual IExprOpenRangeList *mkExprOpenRangeList() = 0;
    virtual IExprOpenRangeValue *mkExprOpenRangeValue(    IExpr* lhs,
    IExpr* rhs) = 0;
    virtual IExprRefPath *mkExprRefPath() = 0;
    virtual IExprRefPathElem *mkExprRefPathElem() = 0;
    virtual IExprStaticRefPath *mkExprStaticRefPath(    bool is_global,
    IExprMemberPathElem* leaf) = 0;
    virtual IExprString *mkExprString(    std::string value,
    bool is_raw) = 0;
    virtual IExprStructLiteral *mkExprStructLiteral() = 0;
    virtual IExprStructLiteralItem *mkExprStructLiteralItem(    IExprId* id,
    IExpr* value) = 0;
    virtual IExprSubscript *mkExprSubscript(    IExpr* expr,
    IExpr* subscript) = 0;
    virtual IExprUnary *mkExprUnary(    ExprUnaryOp op,
    IExpr* rhs) = 0;
    virtual IExtendEnum *mkExtendEnum(    ITypeIdentifier* target) = 0;
    virtual IFunctionDefinition *mkFunctionDefinition(    IFunctionPrototype* proto,
    IExecScope* body,
    PlatQual plat) = 0;
    virtual IFunctionImport *mkFunctionImport(    PlatQual plat,
    std::string lang) = 0;
    virtual IFunctionParamDecl *mkFunctionParamDecl(    FunctionParamDeclKind kind,
    IExprId* name,
    IDataType* type,
    ParamDir dir,
    IExpr* dflt) = 0;
    virtual IMethodParameterList *mkMethodParameterList() = 0;
    virtual INamedScopeChild *mkNamedScopeChild(    IExprId* name) = 0;
    virtual IPackageImportStmt *mkPackageImportStmt(    bool wildcard,
    IExprId* alias) = 0;
    virtual IProceduralStmtIfClause *mkProceduralStmtIfClause(    IExpr* cond,
    IScopeChild* body) = 0;
    virtual IProceduralStmtMatch *mkProceduralStmtMatch(    IExpr* expr) = 0;
    virtual IProceduralStmtMatchChoice *mkProceduralStmtMatchChoice(    bool is_default,
    IExprOpenRangeList* cond,
    IScopeChild* body) = 0;
    virtual IActivityBindStmt *mkActivityBindStmt(    IExprHierarchicalId* lhs) = 0;
    virtual IActivityConstraint *mkActivityConstraint(    IConstraintStmt* constraint) = 0;
    virtual IProceduralStmtReturn *mkProceduralStmtReturn(    IExpr* expr) = 0;
    virtual IProceduralStmtYield *mkProceduralStmtYield() = 0;
    virtual IActivityLabeledStmt *mkActivityLabeledStmt() = 0;
    virtual ISymbolChildrenScope *mkSymbolChildrenScope(    std::string name) = 0;
    virtual ITemplateCategoryTypeParamDecl *mkTemplateCategoryTypeParamDecl(    IExprId* name,
    TypeCategory category,
    ITypeIdentifier* restriction,
    IDataType* dflt) = 0;
    virtual ITemplateGenericTypeParamDecl *mkTemplateGenericTypeParamDecl(    IExprId* name,
    IDataType* dflt) = 0;
    virtual IConstraintScope *mkConstraintScope() = 0;
    virtual IConstraintStmtDefault *mkConstraintStmtDefault(    IExprHierarchicalId* hid,
    IExpr* expr) = 0;
    virtual IConstraintStmtDefaultDisable *mkConstraintStmtDefaultDisable(    IExprHierarchicalId* hid) = 0;
    virtual IConstraintStmtExpr *mkConstraintStmtExpr(    IExpr* expr) = 0;
    virtual IConstraintStmtField *mkConstraintStmtField(    IExprId* name,
    IDataType* type) = 0;
    virtual ITemplateValueParamDecl *mkTemplateValueParamDecl(    IExprId* name,
    IDataType* type,
    IExpr* dflt) = 0;
    virtual IConstraintStmtIf *mkConstraintStmtIf(    IExpr* cond,
    IConstraintScope* true_c,
    IConstraintScope* false_c) = 0;
    virtual IConstraintStmtUnique *mkConstraintStmtUnique() = 0;
    virtual IDataTypeBool *mkDataTypeBool() = 0;
    virtual IDataTypeChandle *mkDataTypeChandle() = 0;
    virtual IDataTypeEnum *mkDataTypeEnum(    IDataTypeUserDefined* tid,
    IExprOpenRangeList* in_rangelist) = 0;
    virtual IDataTypeInt *mkDataTypeInt(    bool is_signed,
    IExpr* width,
    IExprDomainOpenRangeList* in_range) = 0;
    virtual IDataTypePyObj *mkDataTypePyObj() = 0;
    virtual IDataTypeRef *mkDataTypeRef(    IDataTypeUserDefined* type) = 0;
    virtual IDataTypeString *mkDataTypeString(    bool has_range) = 0;
    virtual IDataTypeUserDefined *mkDataTypeUserDefined(    bool is_global,
    ITypeIdentifier* type_id) = 0;
    virtual IEnumDecl *mkEnumDecl(    IExprId* name) = 0;
    virtual IEnumItem *mkEnumItem(    IExprId* name,
    IExpr* value) = 0;
    virtual IExprAggrEmpty *mkExprAggrEmpty() = 0;
    virtual IExprAggrList *mkExprAggrList() = 0;
    virtual IExprAggrMap *mkExprAggrMap() = 0;
    virtual IExprAggrStruct *mkExprAggrStruct() = 0;
    virtual IExprRefPathContext *mkExprRefPathContext(    IExprHierarchicalId* hier_id) = 0;
    virtual IExprRefPathId *mkExprRefPathId(    IExprId* id) = 0;
    virtual IExprRefPathStatic *mkExprRefPathStatic(    bool is_global) = 0;
    virtual IExprRefPathStaticRooted *mkExprRefPathStaticRooted(    IExprRefPathStatic* root,
    IExprHierarchicalId* leaf) = 0;
    virtual IExprSignedNumber *mkExprSignedNumber(    std::string image,
    int32_t width,
    int64_t value) = 0;
    virtual IExprUnsignedNumber *mkExprUnsignedNumber(    std::string image,
    int32_t width,
    uint64_t value) = 0;
    virtual IExtendType *mkExtendType(    ExtendTargetE kind,
    ITypeIdentifier* target) = 0;
    virtual IField *mkField(    IExprId* name,
    IDataType* type,
    FieldAttr attr,
    IExpr* init) = 0;
    virtual IFieldClaim *mkFieldClaim(    IExprId* name,
    IDataTypeUserDefined* type,
    bool is_lock) = 0;
    virtual IFieldCompRef *mkFieldCompRef(    IExprId* name,
    IDataTypeUserDefined* type) = 0;
    virtual IFieldRef *mkFieldRef(    IExprId* name,
    IDataTypeUserDefined* type,
    bool is_input) = 0;
    virtual IFunctionImportProto *mkFunctionImportProto(    PlatQual plat,
    std::string lang,
    IFunctionPrototype* proto) = 0;
    virtual IFunctionImportType *mkFunctionImportType(    PlatQual plat,
    std::string lang,
    ITypeIdentifier* type) = 0;
    virtual IFunctionPrototype *mkFunctionPrototype(    IExprId* name,
    IDataType* rtype,
    bool is_target,
    bool is_solve) = 0;
    virtual IGlobalScope *mkGlobalScope(    int32_t fileid) = 0;
    virtual INamedScope *mkNamedScope(    IExprId* name) = 0;
    virtual IPackageScope *mkPackageScope() = 0;
    virtual IProceduralStmtAssignment *mkProceduralStmtAssignment(    IExpr* lhs,
    AssignOp op,
    IExpr* rhs) = 0;
    virtual IProceduralStmtBody *mkProceduralStmtBody(    IScopeChild* body) = 0;
    virtual IProceduralStmtBreak *mkProceduralStmtBreak() = 0;
    virtual IProceduralStmtContinue *mkProceduralStmtContinue() = 0;
    virtual IProceduralStmtDataDeclaration *mkProceduralStmtDataDeclaration(    IExprId* name,
    IDataType* datatype,
    IExpr* init) = 0;
    virtual IProceduralStmtExpr *mkProceduralStmtExpr(    IExpr* expr) = 0;
    virtual IProceduralStmtFunctionCall *mkProceduralStmtFunctionCall(    IExprRefPathStaticRooted* prefix) = 0;
    virtual IProceduralStmtIfElse *mkProceduralStmtIfElse() = 0;
    virtual IActivityActionHandleTraversal *mkActivityActionHandleTraversal(    IExprRefPathContext* target,
    IConstraintStmt* with_c) = 0;
    virtual IActivityActionTypeTraversal *mkActivityActionTypeTraversal(    IDataTypeUserDefined* target,
    IConstraintStmt* with_c) = 0;
    virtual IProceduralStmtRepeatWhile *mkProceduralStmtRepeatWhile(    IScopeChild* body,
    IExpr* expr) = 0;
    virtual IActivityForeach *mkActivityForeach(    IExprId* it_id,
    IExprId* idx_id,
    IExprRefPathContext* target,
    IScopeChild* body) = 0;
    virtual IActivityIfElse *mkActivityIfElse(    IExpr* cond,
    IActivityStmt* true_s,
    IActivityStmt* false_s) = 0;
    virtual IProceduralStmtWhile *mkProceduralStmtWhile(    IScopeChild* body,
    IExpr* expr) = 0;
    virtual IActivityMatch *mkActivityMatch(    IExpr* cond) = 0;
    virtual IActivityRepeatCount *mkActivityRepeatCount(    IExprId* loop_var,
    IExpr* count,
    IScopeChild* body) = 0;
    virtual IActivityRepeatWhile *mkActivityRepeatWhile(    IExpr* cond,
    IScopeChild* body) = 0;
    virtual IActivityReplicate *mkActivityReplicate(    IExprId* idx_id,
    IExprId* it_label,
    IScopeChild* body) = 0;
    virtual IActivitySelect *mkActivitySelect() = 0;
    virtual ISymbolScope *mkSymbolScope(    std::string name) = 0;
    virtual IActivitySuper *mkActivitySuper() = 0;
    virtual IConstraintBlock *mkConstraintBlock(    std::string name,
    bool is_dynamic) = 0;
    virtual IConstraintStmtForall *mkConstraintStmtForall(    IExprId* iterator_id,
    IDataTypeUserDefined* type_id,
    IExprRefPath* ref_path) = 0;
    virtual IConstraintStmtForeach *mkConstraintStmtForeach(    IExpr* expr) = 0;
    virtual IConstraintStmtImplication *mkConstraintStmtImplication(    IExpr* cond) = 0;
    virtual ITypeScope *mkTypeScope(    IExprId* name,
    ITypeIdentifier* super_t) = 0;
    virtual IExprRefPathStaticFunc *mkExprRefPathStaticFunc(    bool is_global,
    IMethodParameterList* params) = 0;
    virtual IExprRefPathSuper *mkExprRefPathSuper(    IExprHierarchicalId* hier_id) = 0;
    virtual IAction *mkAction(    IExprId* name,
    ITypeIdentifier* super_t,
    bool is_abstract) = 0;
    virtual IActivityDecl *mkActivityDecl(    std::string name) = 0;
    virtual IProceduralStmtSymbolBodyScope *mkProceduralStmtSymbolBodyScope(    std::string name,
    IScopeChild* body) = 0;
    virtual IConstraintSymbolScope *mkConstraintSymbolScope(    std::string name) = 0;
    virtual IActivityLabeledScope *mkActivityLabeledScope(    std::string name) = 0;
    virtual IRootSymbolScope *mkRootSymbolScope(    std::string name) = 0;
    virtual IStruct *mkStruct(    IExprId* name,
    ITypeIdentifier* super_t,
    StructKind kind) = 0;
    virtual ISymbolEnumScope *mkSymbolEnumScope(    std::string name) = 0;
    virtual ISymbolExtendScope *mkSymbolExtendScope(    std::string name) = 0;
    virtual IExecScope *mkExecScope(    std::string name) = 0;
    virtual ISymbolFunctionScope *mkSymbolFunctionScope(    std::string name) = 0;
    virtual ISymbolTypeScope *mkSymbolTypeScope(    std::string name,
    ISymbolScope* plist) = 0;
    virtual IComponent *mkComponent(    IExprId* name,
    ITypeIdentifier* super_t) = 0;
    virtual IProceduralStmtRepeat *mkProceduralStmtRepeat(    std::string name,
    IScopeChild* body,
    IExprId* it_id,
    IExpr* count) = 0;
    virtual IActivityParallel *mkActivityParallel(    std::string name,
    IActivityJoinSpec* join_spec) = 0;
    virtual IActivitySchedule *mkActivitySchedule(    std::string name,
    IActivityJoinSpec* join_spec) = 0;
    virtual IExecBlock *mkExecBlock(    std::string name,
    ExecKind kind) = 0;
    virtual IActivitySequence *mkActivitySequence(    std::string name) = 0;
    virtual IProceduralStmtForeach *mkProceduralStmtForeach(    std::string name,
    IScopeChild* body,
    IExprRefPath* path,
    IExprId* it_id,
    IExprId* idx_id) = 0;
};

} // namespace zsp
} // namespace ast

