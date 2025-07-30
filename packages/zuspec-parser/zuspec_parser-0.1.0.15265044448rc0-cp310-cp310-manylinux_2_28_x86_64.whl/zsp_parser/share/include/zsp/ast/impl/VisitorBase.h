/****************************************************************************
 * VisitorBase.h
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
#include "zsp/ast/IVisitor.h"

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


class VisitorBase : public virtual IVisitor {
public:
    VisitorBase(IVisitor *this_p=0) : m_this(this_p?this_p:this) { }
    
    virtual ~VisitorBase() { }
    
    virtual void visitExprAggrMapElem(IExprAggrMapElem *i) override {
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitTemplateParamDeclList(ITemplateParamDeclList *i) override {
        for (std::vector<ITemplateParamDeclUP>::const_iterator
                it=i->getParams().begin();
                it!=i->getParams().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprAggrStructElem(IExprAggrStructElem *i) override {
        if (i->getName()) {
            i->getName()->accept(this);
        }
        if (i->getValue()) {
            i->getValue()->accept(this);
        }
    }
    
    virtual void visitTemplateParamValue(ITemplateParamValue *i) override {
    }
    
    virtual void visitTemplateParamValueList(ITemplateParamValueList *i) override {
        for (std::vector<ITemplateParamValueUP>::const_iterator
                it=i->getValues().begin();
                it!=i->getValues().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitActivityJoinSpec(IActivityJoinSpec *i) override {
    }
    
    virtual void visitRefExpr(IRefExpr *i) override {
    }
    
    virtual void visitActivityMatchChoice(IActivityMatchChoice *i) override {
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitScopeChild(IScopeChild *i) override {
        if (i->getAssocData()) {
            i->getAssocData()->accept(this);
        }
    }
    
    virtual void visitActivitySelectBranch(IActivitySelectBranch *i) override {
        if (i->getGuard()) {
            i->getGuard()->accept(this);
        }
        if (i->getWeight()) {
            i->getWeight()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitSymbolRefPath(ISymbolRefPath *i) override {
    }
    
    virtual void visitExecTargetTemplateParam(IExecTargetTemplateParam *i) override {
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitExpr(IExpr *i) override {
    }
    
    virtual void visitAssocData(IAssocData *i) override {
    }
    
    virtual void visitSymbolImportSpec(ISymbolImportSpec *i) override {
        for (std::vector<IPackageImportStmt *>::const_iterator
                it=i->getImports().begin();
                it!=i->getImports().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitPyImportFromStmt(IPyImportFromStmt *i) override {
        visitScopeChild(i);
        for (std::vector<IExprIdUP>::const_iterator
                it=i->getPath().begin();
                it!=i->getPath().end(); it++) {
            (*it)->accept(this);
        }
        for (std::vector<IExprIdUP>::const_iterator
                it=i->getTargets().begin();
                it!=i->getTargets().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitActivityJoinSpecBranch(IActivityJoinSpecBranch *i) override {
        visitActivityJoinSpec(i);
        for (std::vector<IExprRefPathContextUP>::const_iterator
                it=i->getBranches().begin();
                it!=i->getBranches().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitActivityJoinSpecFirst(IActivityJoinSpecFirst *i) override {
        visitActivityJoinSpec(i);
        if (i->getCount()) {
            i->getCount()->accept(this);
        }
    }
    
    virtual void visitActivityJoinSpecNone(IActivityJoinSpecNone *i) override {
        visitActivityJoinSpec(i);
    }
    
    virtual void visitActivityJoinSpecSelect(IActivityJoinSpecSelect *i) override {
        visitActivityJoinSpec(i);
        if (i->getCount()) {
            i->getCount()->accept(this);
        }
    }
    
    virtual void visitPyImportStmt(IPyImportStmt *i) override {
        visitScopeChild(i);
        for (std::vector<IExprIdUP>::const_iterator
                it=i->getPath().begin();
                it!=i->getPath().end(); it++) {
            (*it)->accept(this);
        }
        if (i->getAlias()) {
            i->getAlias()->accept(this);
        }
    }
    
    virtual void visitRefExprScopeIndex(IRefExprScopeIndex *i) override {
        visitRefExpr(i);
        if (i->getBase()) {
            i->getBase()->accept(this);
        }
    }
    
    virtual void visitRefExprTypeScopeContext(IRefExprTypeScopeContext *i) override {
        visitRefExpr(i);
        if (i->getBase()) {
            i->getBase()->accept(this);
        }
    }
    
    virtual void visitRefExprTypeScopeGlobal(IRefExprTypeScopeGlobal *i) override {
        visitRefExpr(i);
    }
    
    virtual void visitScope(IScope *i) override {
        visitScopeChild(i);
        for (std::vector<IScopeChildUP>::const_iterator
                it=i->getChildren().begin();
                it!=i->getChildren().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitScopeChildRef(IScopeChildRef *i) override {
        visitScopeChild(i);
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
    }
    
    virtual void visitSymbolChild(ISymbolChild *i) override {
        visitScopeChild(i);
    }
    
    virtual void visitActivitySchedulingConstraint(IActivitySchedulingConstraint *i) override {
        visitScopeChild(i);
        for (std::vector<IExprHierarchicalIdUP>::const_iterator
                it=i->getTargets().begin();
                it!=i->getTargets().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitActivityStmt(IActivityStmt *i) override {
        visitScopeChild(i);
    }
    
    virtual void visitSymbolScopeRef(ISymbolScopeRef *i) override {
        visitScopeChild(i);
    }
    
    virtual void visitTemplateParamDecl(ITemplateParamDecl *i) override {
        visitScopeChild(i);
        if (i->getName()) {
            i->getName()->accept(this);
        }
    }
    
    virtual void visitConstraintStmt(IConstraintStmt *i) override {
        visitScopeChild(i);
    }
    
    virtual void visitTemplateParamExprValue(ITemplateParamExprValue *i) override {
        visitTemplateParamValue(i);
        if (i->getValue()) {
            i->getValue()->accept(this);
        }
    }
    
    virtual void visitTemplateParamTypeValue(ITemplateParamTypeValue *i) override {
        visitTemplateParamValue(i);
        if (i->getValue()) {
            i->getValue()->accept(this);
        }
    }
    
    virtual void visitTypeIdentifier(ITypeIdentifier *i) override {
        visitExpr(i);
        for (std::vector<ITypeIdentifierElemUP>::const_iterator
                it=i->getElems().begin();
                it!=i->getElems().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitTypeIdentifierElem(ITypeIdentifierElem *i) override {
        visitExpr(i);
        if (i->getId()) {
            i->getId()->accept(this);
        }
        if (i->getParams()) {
            i->getParams()->accept(this);
        }
    }
    
    virtual void visitDataType(IDataType *i) override {
        visitScopeChild(i);
    }
    
    virtual void visitExecStmt(IExecStmt *i) override {
        visitScopeChild(i);
    }
    
    virtual void visitExecTargetTemplateBlock(IExecTargetTemplateBlock *i) override {
        visitScopeChild(i);
        for (std::vector<IExecTargetTemplateParamUP>::const_iterator
                it=i->getParameters().begin();
                it!=i->getParameters().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprAggrLiteral(IExprAggrLiteral *i) override {
        visitExpr(i);
    }
    
    virtual void visitExprBin(IExprBin *i) override {
        visitExpr(i);
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitExprBitSlice(IExprBitSlice *i) override {
        visitExpr(i);
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitExprBool(IExprBool *i) override {
        visitExpr(i);
    }
    
    virtual void visitExprCast(IExprCast *i) override {
        visitExpr(i);
        if (i->getCasting_type()) {
            i->getCasting_type()->accept(this);
        }
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitExprCompileHas(IExprCompileHas *i) override {
        visitExpr(i);
        if (i->getRef()) {
            i->getRef()->accept(this);
        }
    }
    
    virtual void visitExprCond(IExprCond *i) override {
        visitExpr(i);
        if (i->getCond_e()) {
            i->getCond_e()->accept(this);
        }
        if (i->getTrue_e()) {
            i->getTrue_e()->accept(this);
        }
        if (i->getFalse_e()) {
            i->getFalse_e()->accept(this);
        }
    }
    
    virtual void visitExprDomainOpenRangeList(IExprDomainOpenRangeList *i) override {
        visitExpr(i);
        for (std::vector<IExprDomainOpenRangeValueUP>::const_iterator
                it=i->getValues().begin();
                it!=i->getValues().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprDomainOpenRangeValue(IExprDomainOpenRangeValue *i) override {
        visitExpr(i);
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitExprHierarchicalId(IExprHierarchicalId *i) override {
        visitExpr(i);
        for (std::vector<IExprMemberPathElemUP>::const_iterator
                it=i->getElems().begin();
                it!=i->getElems().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprId(IExprId *i) override {
        visitExpr(i);
    }
    
    virtual void visitExprIn(IExprIn *i) override {
        visitExpr(i);
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitExprListLiteral(IExprListLiteral *i) override {
        visitExpr(i);
        for (std::vector<IExprUP>::const_iterator
                it=i->getValue().begin();
                it!=i->getValue().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprMemberPathElem(IExprMemberPathElem *i) override {
        visitExpr(i);
        if (i->getId()) {
            i->getId()->accept(this);
        }
        if (i->getParams()) {
            i->getParams()->accept(this);
        }
        for (std::vector<IExprUP>::const_iterator
                it=i->getSubscript().begin();
                it!=i->getSubscript().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprNull(IExprNull *i) override {
        visitExpr(i);
    }
    
    virtual void visitExprNumber(IExprNumber *i) override {
        visitExpr(i);
    }
    
    virtual void visitExprOpenRangeList(IExprOpenRangeList *i) override {
        visitExpr(i);
        for (std::vector<IExprOpenRangeValueUP>::const_iterator
                it=i->getValues().begin();
                it!=i->getValues().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprOpenRangeValue(IExprOpenRangeValue *i) override {
        visitExpr(i);
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitExprRefPath(IExprRefPath *i) override {
        visitExpr(i);
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
    }
    
    virtual void visitExprRefPathElem(IExprRefPathElem *i) override {
        visitExpr(i);
    }
    
    virtual void visitExprStaticRefPath(IExprStaticRefPath *i) override {
        visitExpr(i);
        for (std::vector<ITypeIdentifierElemUP>::const_iterator
                it=i->getBase().begin();
                it!=i->getBase().end(); it++) {
            (*it)->accept(this);
        }
        if (i->getLeaf()) {
            i->getLeaf()->accept(this);
        }
    }
    
    virtual void visitExprString(IExprString *i) override {
        visitExpr(i);
    }
    
    virtual void visitExprStructLiteral(IExprStructLiteral *i) override {
        visitExpr(i);
        for (std::vector<IExprStructLiteralItemUP>::const_iterator
                it=i->getValues().begin();
                it!=i->getValues().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprStructLiteralItem(IExprStructLiteralItem *i) override {
        visitExpr(i);
        if (i->getId()) {
            i->getId()->accept(this);
        }
        if (i->getValue()) {
            i->getValue()->accept(this);
        }
    }
    
    virtual void visitExprSubscript(IExprSubscript *i) override {
        visitExpr(i);
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
        if (i->getSubscript()) {
            i->getSubscript()->accept(this);
        }
    }
    
    virtual void visitExprUnary(IExprUnary *i) override {
        visitExpr(i);
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitExtendEnum(IExtendEnum *i) override {
        visitScopeChild(i);
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
        for (std::vector<IEnumItemUP>::const_iterator
                it=i->getItems().begin();
                it!=i->getItems().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitFunctionDefinition(IFunctionDefinition *i) override {
        visitScopeChild(i);
        if (i->getProto()) {
            i->getProto()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitFunctionImport(IFunctionImport *i) override {
        visitScopeChild(i);
    }
    
    virtual void visitFunctionParamDecl(IFunctionParamDecl *i) override {
        visitScopeChild(i);
        if (i->getName()) {
            i->getName()->accept(this);
        }
        if (i->getType()) {
            i->getType()->accept(this);
        }
        if (i->getDflt()) {
            i->getDflt()->accept(this);
        }
    }
    
    virtual void visitMethodParameterList(IMethodParameterList *i) override {
        visitExpr(i);
        for (std::vector<IExprUP>::const_iterator
                it=i->getParameters().begin();
                it!=i->getParameters().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitNamedScopeChild(INamedScopeChild *i) override {
        visitScopeChild(i);
        if (i->getName()) {
            i->getName()->accept(this);
        }
    }
    
    virtual void visitPackageImportStmt(IPackageImportStmt *i) override {
        visitScopeChild(i);
        if (i->getAlias()) {
            i->getAlias()->accept(this);
        }
        if (i->getPath()) {
            i->getPath()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtIfClause(IProceduralStmtIfClause *i) override {
        visitScopeChild(i);
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtMatch(IProceduralStmtMatch *i) override {
        visitExecStmt(i);
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
        for (std::vector<IProceduralStmtMatchChoiceUP>::const_iterator
                it=i->getChoices().begin();
                it!=i->getChoices().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitProceduralStmtMatchChoice(IProceduralStmtMatchChoice *i) override {
        visitExecStmt(i);
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitActivityBindStmt(IActivityBindStmt *i) override {
        visitActivityStmt(i);
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        for (std::vector<IExprHierarchicalIdUP>::const_iterator
                it=i->getRhs().begin();
                it!=i->getRhs().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitActivityConstraint(IActivityConstraint *i) override {
        visitActivityStmt(i);
        if (i->getConstraint()) {
            i->getConstraint()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtReturn(IProceduralStmtReturn *i) override {
        visitExecStmt(i);
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtYield(IProceduralStmtYield *i) override {
        visitExecStmt(i);
    }
    
    virtual void visitActivityLabeledStmt(IActivityLabeledStmt *i) override {
        visitActivityStmt(i);
        if (i->getLabel()) {
            i->getLabel()->accept(this);
        }
    }
    
    virtual void visitSymbolChildrenScope(ISymbolChildrenScope *i) override {
        visitSymbolChild(i);
        for (std::vector<IScopeChildUP>::const_iterator
                it=i->getChildren().begin();
                it!=i->getChildren().end(); it++) {
            (*it)->accept(this);
        }
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
    }
    
    virtual void visitTemplateCategoryTypeParamDecl(ITemplateCategoryTypeParamDecl *i) override {
        visitTemplateParamDecl(i);
        if (i->getRestriction()) {
            i->getRestriction()->accept(this);
        }
        if (i->getDflt()) {
            i->getDflt()->accept(this);
        }
    }
    
    virtual void visitTemplateGenericTypeParamDecl(ITemplateGenericTypeParamDecl *i) override {
        visitTemplateParamDecl(i);
        if (i->getDflt()) {
            i->getDflt()->accept(this);
        }
    }
    
    virtual void visitConstraintScope(IConstraintScope *i) override {
        visitConstraintStmt(i);
        for (std::vector<IConstraintStmtUP>::const_iterator
                it=i->getConstraints().begin();
                it!=i->getConstraints().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitConstraintStmtDefault(IConstraintStmtDefault *i) override {
        visitConstraintStmt(i);
        if (i->getHid()) {
            i->getHid()->accept(this);
        }
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitConstraintStmtDefaultDisable(IConstraintStmtDefaultDisable *i) override {
        visitConstraintStmt(i);
        if (i->getHid()) {
            i->getHid()->accept(this);
        }
    }
    
    virtual void visitConstraintStmtExpr(IConstraintStmtExpr *i) override {
        visitConstraintStmt(i);
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitConstraintStmtField(IConstraintStmtField *i) override {
        visitConstraintStmt(i);
        if (i->getName()) {
            i->getName()->accept(this);
        }
        if (i->getType()) {
            i->getType()->accept(this);
        }
    }
    
    virtual void visitTemplateValueParamDecl(ITemplateValueParamDecl *i) override {
        visitTemplateParamDecl(i);
        if (i->getType()) {
            i->getType()->accept(this);
        }
        if (i->getDflt()) {
            i->getDflt()->accept(this);
        }
    }
    
    virtual void visitConstraintStmtIf(IConstraintStmtIf *i) override {
        visitConstraintStmt(i);
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
        if (i->getTrue_c()) {
            i->getTrue_c()->accept(this);
        }
        if (i->getFalse_c()) {
            i->getFalse_c()->accept(this);
        }
    }
    
    virtual void visitConstraintStmtUnique(IConstraintStmtUnique *i) override {
        visitConstraintStmt(i);
        for (std::vector<IExprHierarchicalIdUP>::const_iterator
                it=i->getList().begin();
                it!=i->getList().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitDataTypeBool(IDataTypeBool *i) override {
        visitDataType(i);
    }
    
    virtual void visitDataTypeChandle(IDataTypeChandle *i) override {
        visitDataType(i);
    }
    
    virtual void visitDataTypeEnum(IDataTypeEnum *i) override {
        visitDataType(i);
        if (i->getTid()) {
            i->getTid()->accept(this);
        }
        if (i->getIn_rangelist()) {
            i->getIn_rangelist()->accept(this);
        }
    }
    
    virtual void visitDataTypeInt(IDataTypeInt *i) override {
        visitDataType(i);
        if (i->getWidth()) {
            i->getWidth()->accept(this);
        }
        if (i->getIn_range()) {
            i->getIn_range()->accept(this);
        }
    }
    
    virtual void visitDataTypePyObj(IDataTypePyObj *i) override {
        visitDataType(i);
    }
    
    virtual void visitDataTypeRef(IDataTypeRef *i) override {
        visitDataType(i);
        if (i->getType()) {
            i->getType()->accept(this);
        }
    }
    
    virtual void visitDataTypeString(IDataTypeString *i) override {
        visitDataType(i);
    }
    
    virtual void visitDataTypeUserDefined(IDataTypeUserDefined *i) override {
        visitDataType(i);
        if (i->getType_id()) {
            i->getType_id()->accept(this);
        }
    }
    
    virtual void visitEnumDecl(IEnumDecl *i) override {
        visitNamedScopeChild(i);
        for (std::vector<IEnumItemUP>::const_iterator
                it=i->getItems().begin();
                it!=i->getItems().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitEnumItem(IEnumItem *i) override {
        visitNamedScopeChild(i);
        if (i->getValue()) {
            i->getValue()->accept(this);
        }
    }
    
    virtual void visitExprAggrEmpty(IExprAggrEmpty *i) override {
        visitExprAggrLiteral(i);
    }
    
    virtual void visitExprAggrList(IExprAggrList *i) override {
        visitExprAggrLiteral(i);
        for (std::vector<IExprUP>::const_iterator
                it=i->getElems().begin();
                it!=i->getElems().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprAggrMap(IExprAggrMap *i) override {
        visitExprAggrLiteral(i);
        for (std::vector<IExprAggrMapElemUP>::const_iterator
                it=i->getElems().begin();
                it!=i->getElems().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprAggrStruct(IExprAggrStruct *i) override {
        visitExprAggrLiteral(i);
        for (std::vector<IExprAggrStructElemUP>::const_iterator
                it=i->getElems().begin();
                it!=i->getElems().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitExprRefPathContext(IExprRefPathContext *i) override {
        visitExprRefPath(i);
        if (i->getHier_id()) {
            i->getHier_id()->accept(this);
        }
        if (i->getSlice()) {
            i->getSlice()->accept(this);
        }
    }
    
    virtual void visitExprRefPathId(IExprRefPathId *i) override {
        visitExprRefPath(i);
        if (i->getId()) {
            i->getId()->accept(this);
        }
        if (i->getSlice()) {
            i->getSlice()->accept(this);
        }
    }
    
    virtual void visitExprRefPathStatic(IExprRefPathStatic *i) override {
        visitExprRefPath(i);
        for (std::vector<ITypeIdentifierElemUP>::const_iterator
                it=i->getBase().begin();
                it!=i->getBase().end(); it++) {
            (*it)->accept(this);
        }
        if (i->getSlice()) {
            i->getSlice()->accept(this);
        }
    }
    
    virtual void visitExprRefPathStaticRooted(IExprRefPathStaticRooted *i) override {
        visitExprRefPath(i);
        if (i->getRoot()) {
            i->getRoot()->accept(this);
        }
        if (i->getLeaf()) {
            i->getLeaf()->accept(this);
        }
        if (i->getSlice()) {
            i->getSlice()->accept(this);
        }
    }
    
    virtual void visitExprSignedNumber(IExprSignedNumber *i) override {
        visitExprNumber(i);
    }
    
    virtual void visitExprUnsignedNumber(IExprUnsignedNumber *i) override {
        visitExprNumber(i);
    }
    
    virtual void visitExtendType(IExtendType *i) override {
        visitScope(i);
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
        if (i->getImports()) {
            i->getImports()->accept(this);
        }
    }
    
    virtual void visitField(IField *i) override {
        visitNamedScopeChild(i);
        if (i->getType()) {
            i->getType()->accept(this);
        }
        if (i->getInit()) {
            i->getInit()->accept(this);
        }
    }
    
    virtual void visitFieldClaim(IFieldClaim *i) override {
        visitNamedScopeChild(i);
        if (i->getType()) {
            i->getType()->accept(this);
        }
    }
    
    virtual void visitFieldCompRef(IFieldCompRef *i) override {
        visitNamedScopeChild(i);
        if (i->getType()) {
            i->getType()->accept(this);
        }
    }
    
    virtual void visitFieldRef(IFieldRef *i) override {
        visitNamedScopeChild(i);
        if (i->getType()) {
            i->getType()->accept(this);
        }
    }
    
    virtual void visitFunctionImportProto(IFunctionImportProto *i) override {
        visitFunctionImport(i);
        if (i->getProto()) {
            i->getProto()->accept(this);
        }
    }
    
    virtual void visitFunctionImportType(IFunctionImportType *i) override {
        visitFunctionImport(i);
        if (i->getType()) {
            i->getType()->accept(this);
        }
    }
    
    virtual void visitFunctionPrototype(IFunctionPrototype *i) override {
        visitNamedScopeChild(i);
        if (i->getRtype()) {
            i->getRtype()->accept(this);
        }
        for (std::vector<IFunctionParamDeclUP>::const_iterator
                it=i->getParameters().begin();
                it!=i->getParameters().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitGlobalScope(IGlobalScope *i) override {
        visitScope(i);
    }
    
    virtual void visitNamedScope(INamedScope *i) override {
        visitScope(i);
        if (i->getName()) {
            i->getName()->accept(this);
        }
    }
    
    virtual void visitPackageScope(IPackageScope *i) override {
        visitScope(i);
        for (std::vector<IExprIdUP>::const_iterator
                it=i->getId().begin();
                it!=i->getId().end(); it++) {
            (*it)->accept(this);
        }
        if (i->getSibling()) {
            i->getSibling()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtAssignment(IProceduralStmtAssignment *i) override {
        visitExecStmt(i);
        if (i->getLhs()) {
            i->getLhs()->accept(this);
        }
        if (i->getRhs()) {
            i->getRhs()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtBody(IProceduralStmtBody *i) override {
        visitExecStmt(i);
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtBreak(IProceduralStmtBreak *i) override {
        visitExecStmt(i);
    }
    
    virtual void visitProceduralStmtContinue(IProceduralStmtContinue *i) override {
        visitExecStmt(i);
    }
    
    virtual void visitProceduralStmtDataDeclaration(IProceduralStmtDataDeclaration *i) override {
        visitExecStmt(i);
        if (i->getName()) {
            i->getName()->accept(this);
        }
        if (i->getDatatype()) {
            i->getDatatype()->accept(this);
        }
        if (i->getInit()) {
            i->getInit()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtExpr(IProceduralStmtExpr *i) override {
        visitExecStmt(i);
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtFunctionCall(IProceduralStmtFunctionCall *i) override {
        visitExecStmt(i);
        if (i->getPrefix()) {
            i->getPrefix()->accept(this);
        }
        for (std::vector<IExprUP>::const_iterator
                it=i->getParams().begin();
                it!=i->getParams().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitProceduralStmtIfElse(IProceduralStmtIfElse *i) override {
        visitExecStmt(i);
        for (std::vector<IProceduralStmtIfClauseUP>::const_iterator
                it=i->getIf_then().begin();
                it!=i->getIf_then().end(); it++) {
            (*it)->accept(this);
        }
        if (i->getElse_then()) {
            i->getElse_then()->accept(this);
        }
    }
    
    virtual void visitActivityActionHandleTraversal(IActivityActionHandleTraversal *i) override {
        visitActivityLabeledStmt(i);
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
        if (i->getWith_c()) {
            i->getWith_c()->accept(this);
        }
    }
    
    virtual void visitActivityActionTypeTraversal(IActivityActionTypeTraversal *i) override {
        visitActivityLabeledStmt(i);
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
        if (i->getWith_c()) {
            i->getWith_c()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtRepeatWhile(IProceduralStmtRepeatWhile *i) override {
        visitProceduralStmtBody(i);
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitActivityForeach(IActivityForeach *i) override {
        visitActivityLabeledStmt(i);
        if (i->getIt_id()) {
            i->getIt_id()->accept(this);
        }
        if (i->getIdx_id()) {
            i->getIdx_id()->accept(this);
        }
        if (i->getTarget()) {
            i->getTarget()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitActivityIfElse(IActivityIfElse *i) override {
        visitActivityLabeledStmt(i);
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
        if (i->getTrue_s()) {
            i->getTrue_s()->accept(this);
        }
        if (i->getFalse_s()) {
            i->getFalse_s()->accept(this);
        }
    }
    
    virtual void visitProceduralStmtWhile(IProceduralStmtWhile *i) override {
        visitProceduralStmtBody(i);
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitActivityMatch(IActivityMatch *i) override {
        visitActivityLabeledStmt(i);
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
        for (std::vector<IActivityMatchChoiceUP>::const_iterator
                it=i->getChoices().begin();
                it!=i->getChoices().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitActivityRepeatCount(IActivityRepeatCount *i) override {
        visitActivityLabeledStmt(i);
        if (i->getLoop_var()) {
            i->getLoop_var()->accept(this);
        }
        if (i->getCount()) {
            i->getCount()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitActivityRepeatWhile(IActivityRepeatWhile *i) override {
        visitActivityLabeledStmt(i);
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitActivityReplicate(IActivityReplicate *i) override {
        visitActivityLabeledStmt(i);
        if (i->getIdx_id()) {
            i->getIdx_id()->accept(this);
        }
        if (i->getIt_label()) {
            i->getIt_label()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitActivitySelect(IActivitySelect *i) override {
        visitActivityLabeledStmt(i);
        for (std::vector<IActivitySelectBranchUP>::const_iterator
                it=i->getBranches().begin();
                it!=i->getBranches().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitSymbolScope(ISymbolScope *i) override {
        visitSymbolChildrenScope(i);
        if (i->getImports()) {
            i->getImports()->accept(this);
        }
    }
    
    virtual void visitActivitySuper(IActivitySuper *i) override {
        visitActivityLabeledStmt(i);
    }
    
    virtual void visitConstraintBlock(IConstraintBlock *i) override {
        visitConstraintScope(i);
    }
    
    virtual void visitConstraintStmtForall(IConstraintStmtForall *i) override {
        visitConstraintScope(i);
        if (i->getIterator_id()) {
            i->getIterator_id()->accept(this);
        }
        if (i->getType_id()) {
            i->getType_id()->accept(this);
        }
        if (i->getRef_path()) {
            i->getRef_path()->accept(this);
        }
        if (i->getSymtab()) {
            i->getSymtab()->accept(this);
        }
    }
    
    virtual void visitConstraintStmtForeach(IConstraintStmtForeach *i) override {
        visitConstraintScope(i);
        if (i->getIt()) {
            i->getIt()->accept(this);
        }
        if (i->getIdx()) {
            i->getIdx()->accept(this);
        }
        if (i->getExpr()) {
            i->getExpr()->accept(this);
        }
    }
    
    virtual void visitConstraintStmtImplication(IConstraintStmtImplication *i) override {
        visitConstraintScope(i);
        if (i->getCond()) {
            i->getCond()->accept(this);
        }
    }
    
    virtual void visitTypeScope(ITypeScope *i) override {
        visitNamedScope(i);
        if (i->getSuper_t()) {
            i->getSuper_t()->accept(this);
        }
        if (i->getParams()) {
            i->getParams()->accept(this);
        }
    }
    
    virtual void visitExprRefPathStaticFunc(IExprRefPathStaticFunc *i) override {
        visitExprRefPathStatic(i);
        if (i->getParams()) {
            i->getParams()->accept(this);
        }
    }
    
    virtual void visitExprRefPathSuper(IExprRefPathSuper *i) override {
        visitExprRefPathContext(i);
    }
    
    virtual void visitAction(IAction *i) override {
        visitTypeScope(i);
    }
    
    virtual void visitActivityDecl(IActivityDecl *i) override {
        visitSymbolScope(i);
    }
    
    virtual void visitProceduralStmtSymbolBodyScope(IProceduralStmtSymbolBodyScope *i) override {
        visitSymbolScope(i);
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitConstraintSymbolScope(IConstraintSymbolScope *i) override {
        visitSymbolScope(i);
        if (i->getConstraint()) {
            i->getConstraint()->accept(this);
        }
    }
    
    virtual void visitActivityLabeledScope(IActivityLabeledScope *i) override {
        visitSymbolScope(i);
        if (i->getLabel()) {
            i->getLabel()->accept(this);
        }
    }
    
    virtual void visitRootSymbolScope(IRootSymbolScope *i) override {
        visitSymbolScope(i);
        for (std::vector<IGlobalScopeUP>::const_iterator
                it=i->getUnits().begin();
                it!=i->getUnits().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitStruct(IStruct *i) override {
        visitTypeScope(i);
    }
    
    virtual void visitSymbolEnumScope(ISymbolEnumScope *i) override {
        visitSymbolScope(i);
    }
    
    virtual void visitSymbolExtendScope(ISymbolExtendScope *i) override {
        visitSymbolScope(i);
    }
    
    virtual void visitExecScope(IExecScope *i) override {
        visitSymbolScope(i);
    }
    
    virtual void visitSymbolFunctionScope(ISymbolFunctionScope *i) override {
        visitSymbolScope(i);
        for (std::vector<IFunctionPrototype *>::const_iterator
                it=i->getPrototypes().begin();
                it!=i->getPrototypes().end(); it++) {
            (*it)->accept(this);
        }
        for (std::vector<IFunctionImportUP>::const_iterator
                it=i->getImport_specs().begin();
                it!=i->getImport_specs().end(); it++) {
            (*it)->accept(this);
        }
        if (i->getDefinition()) {
            i->getDefinition()->accept(this);
        }
        if (i->getPlist()) {
            i->getPlist()->accept(this);
        }
        if (i->getBody()) {
            i->getBody()->accept(this);
        }
    }
    
    virtual void visitSymbolTypeScope(ISymbolTypeScope *i) override {
        visitSymbolScope(i);
        if (i->getPlist()) {
            i->getPlist()->accept(this);
        }
        for (std::vector<ISymbolTypeScopeUP>::const_iterator
                it=i->getSpec_types().begin();
                it!=i->getSpec_types().end(); it++) {
            (*it)->accept(this);
        }
    }
    
    virtual void visitComponent(IComponent *i) override {
        visitTypeScope(i);
    }
    
    virtual void visitProceduralStmtRepeat(IProceduralStmtRepeat *i) override {
        visitProceduralStmtSymbolBodyScope(i);
        if (i->getIt_id()) {
            i->getIt_id()->accept(this);
        }
        if (i->getCount()) {
            i->getCount()->accept(this);
        }
    }
    
    virtual void visitActivityParallel(IActivityParallel *i) override {
        visitActivityLabeledScope(i);
        if (i->getJoin_spec()) {
            i->getJoin_spec()->accept(this);
        }
    }
    
    virtual void visitActivitySchedule(IActivitySchedule *i) override {
        visitActivityLabeledScope(i);
        if (i->getJoin_spec()) {
            i->getJoin_spec()->accept(this);
        }
    }
    
    virtual void visitExecBlock(IExecBlock *i) override {
        visitExecScope(i);
    }
    
    virtual void visitActivitySequence(IActivitySequence *i) override {
        visitActivityLabeledScope(i);
    }
    
    virtual void visitProceduralStmtForeach(IProceduralStmtForeach *i) override {
        visitProceduralStmtSymbolBodyScope(i);
        if (i->getPath()) {
            i->getPath()->accept(this);
        }
        if (i->getIt_id()) {
            i->getIt_id()->accept(this);
        }
        if (i->getIdx_id()) {
            i->getIdx_id()->accept(this);
        }
    }
    
    
    protected:
        IVisitor *m_this;
};


} // namespace zsp
} // namespace ast

