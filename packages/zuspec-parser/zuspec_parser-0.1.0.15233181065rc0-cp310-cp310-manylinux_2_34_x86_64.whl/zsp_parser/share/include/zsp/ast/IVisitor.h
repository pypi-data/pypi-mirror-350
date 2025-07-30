/****************************************************************************
 * IVisitor.h
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

namespace zsp {
namespace ast {

class IExprAggrMapElem;
class ITemplateParamDeclList;
class IExprAggrStructElem;
class ITemplateParamValue;
class ITemplateParamValueList;
class IActivityJoinSpec;
class IRefExpr;
class IActivityMatchChoice;
class IScopeChild;
class IActivitySelectBranch;
class ISymbolRefPath;
class IExecTargetTemplateParam;
class IExpr;
class IAssocData;
class ISymbolImportSpec;
class IPyImportFromStmt;
class IActivityJoinSpecBranch;
class IActivityJoinSpecFirst;
class IActivityJoinSpecNone;
class IActivityJoinSpecSelect;
class IPyImportStmt;
class IRefExprScopeIndex;
class IRefExprTypeScopeContext;
class IRefExprTypeScopeGlobal;
class IScope;
class IScopeChildRef;
class ISymbolChild;
class IActivitySchedulingConstraint;
class IActivityStmt;
class ISymbolScopeRef;
class ITemplateParamDecl;
class IConstraintStmt;
class ITemplateParamExprValue;
class ITemplateParamTypeValue;
class ITypeIdentifier;
class ITypeIdentifierElem;
class IDataType;
class IExecStmt;
class IExecTargetTemplateBlock;
class IExprAggrLiteral;
class IExprBin;
class IExprBitSlice;
class IExprBool;
class IExprCast;
class IExprCompileHas;
class IExprCond;
class IExprDomainOpenRangeList;
class IExprDomainOpenRangeValue;
class IExprHierarchicalId;
class IExprId;
class IExprIn;
class IExprListLiteral;
class IExprMemberPathElem;
class IExprNull;
class IExprNumber;
class IExprOpenRangeList;
class IExprOpenRangeValue;
class IExprRefPath;
class IExprRefPathElem;
class IExprStaticRefPath;
class IExprString;
class IExprStructLiteral;
class IExprStructLiteralItem;
class IExprSubscript;
class IExprUnary;
class IExtendEnum;
class IFunctionDefinition;
class IFunctionImport;
class IFunctionParamDecl;
class IMethodParameterList;
class INamedScopeChild;
class IPackageImportStmt;
class IProceduralStmtIfClause;
class IProceduralStmtMatch;
class IProceduralStmtMatchChoice;
class IActivityBindStmt;
class IActivityConstraint;
class IProceduralStmtReturn;
class IProceduralStmtYield;
class IActivityLabeledStmt;
class ISymbolChildrenScope;
class ITemplateCategoryTypeParamDecl;
class ITemplateGenericTypeParamDecl;
class IConstraintScope;
class IConstraintStmtDefault;
class IConstraintStmtDefaultDisable;
class IConstraintStmtExpr;
class IConstraintStmtField;
class ITemplateValueParamDecl;
class IConstraintStmtIf;
class IConstraintStmtUnique;
class IDataTypeBool;
class IDataTypeChandle;
class IDataTypeEnum;
class IDataTypeInt;
class IDataTypePyObj;
class IDataTypeRef;
class IDataTypeString;
class IDataTypeUserDefined;
class IEnumDecl;
class IEnumItem;
class IExprAggrEmpty;
class IExprAggrList;
class IExprAggrMap;
class IExprAggrStruct;
class IExprRefPathContext;
class IExprRefPathId;
class IExprRefPathStatic;
class IExprRefPathStaticRooted;
class IExprSignedNumber;
class IExprUnsignedNumber;
class IExtendType;
class IField;
class IFieldClaim;
class IFieldCompRef;
class IFieldRef;
class IFunctionImportProto;
class IFunctionImportType;
class IFunctionPrototype;
class IGlobalScope;
class INamedScope;
class IPackageScope;
class IProceduralStmtAssignment;
class IProceduralStmtBody;
class IProceduralStmtBreak;
class IProceduralStmtContinue;
class IProceduralStmtDataDeclaration;
class IProceduralStmtExpr;
class IProceduralStmtFunctionCall;
class IProceduralStmtIfElse;
class IActivityActionHandleTraversal;
class IActivityActionTypeTraversal;
class IProceduralStmtRepeatWhile;
class IActivityForeach;
class IActivityIfElse;
class IProceduralStmtWhile;
class IActivityMatch;
class IActivityRepeatCount;
class IActivityRepeatWhile;
class IActivityReplicate;
class IActivitySelect;
class ISymbolScope;
class IActivitySuper;
class IConstraintBlock;
class IConstraintStmtForall;
class IConstraintStmtForeach;
class IConstraintStmtImplication;
class ITypeScope;
class IExprRefPathStaticFunc;
class IExprRefPathSuper;
class IAction;
class IActivityDecl;
class IProceduralStmtSymbolBodyScope;
class IConstraintSymbolScope;
class IActivityLabeledScope;
class IRootSymbolScope;
class IStruct;
class ISymbolEnumScope;
class ISymbolExtendScope;
class IExecScope;
class ISymbolFunctionScope;
class ISymbolTypeScope;
class IComponent;
class IProceduralStmtRepeat;
class IActivityParallel;
class IActivitySchedule;
class IExecBlock;
class IActivitySequence;
class IProceduralStmtForeach;

class ExprAggrMapElem;
class TemplateParamDeclList;
class ExprAggrStructElem;
class TemplateParamValue;
class TemplateParamValueList;
class ActivityJoinSpec;
class RefExpr;
class ActivityMatchChoice;
class ScopeChild;
class ActivitySelectBranch;
class SymbolRefPath;
class ExecTargetTemplateParam;
class Expr;
class AssocData;
class SymbolImportSpec;
class PyImportFromStmt;
class ActivityJoinSpecBranch;
class ActivityJoinSpecFirst;
class ActivityJoinSpecNone;
class ActivityJoinSpecSelect;
class PyImportStmt;
class RefExprScopeIndex;
class RefExprTypeScopeContext;
class RefExprTypeScopeGlobal;
class Scope;
class ScopeChildRef;
class SymbolChild;
class ActivitySchedulingConstraint;
class ActivityStmt;
class SymbolScopeRef;
class TemplateParamDecl;
class ConstraintStmt;
class TemplateParamExprValue;
class TemplateParamTypeValue;
class TypeIdentifier;
class TypeIdentifierElem;
class DataType;
class ExecStmt;
class ExecTargetTemplateBlock;
class ExprAggrLiteral;
class ExprBin;
class ExprBitSlice;
class ExprBool;
class ExprCast;
class ExprCompileHas;
class ExprCond;
class ExprDomainOpenRangeList;
class ExprDomainOpenRangeValue;
class ExprHierarchicalId;
class ExprId;
class ExprIn;
class ExprListLiteral;
class ExprMemberPathElem;
class ExprNull;
class ExprNumber;
class ExprOpenRangeList;
class ExprOpenRangeValue;
class ExprRefPath;
class ExprRefPathElem;
class ExprStaticRefPath;
class ExprString;
class ExprStructLiteral;
class ExprStructLiteralItem;
class ExprSubscript;
class ExprUnary;
class ExtendEnum;
class FunctionDefinition;
class FunctionImport;
class FunctionParamDecl;
class MethodParameterList;
class NamedScopeChild;
class PackageImportStmt;
class ProceduralStmtIfClause;
class ProceduralStmtMatch;
class ProceduralStmtMatchChoice;
class ActivityBindStmt;
class ActivityConstraint;
class ProceduralStmtReturn;
class ProceduralStmtYield;
class ActivityLabeledStmt;
class SymbolChildrenScope;
class TemplateCategoryTypeParamDecl;
class TemplateGenericTypeParamDecl;
class ConstraintScope;
class ConstraintStmtDefault;
class ConstraintStmtDefaultDisable;
class ConstraintStmtExpr;
class ConstraintStmtField;
class TemplateValueParamDecl;
class ConstraintStmtIf;
class ConstraintStmtUnique;
class DataTypeBool;
class DataTypeChandle;
class DataTypeEnum;
class DataTypeInt;
class DataTypePyObj;
class DataTypeRef;
class DataTypeString;
class DataTypeUserDefined;
class EnumDecl;
class EnumItem;
class ExprAggrEmpty;
class ExprAggrList;
class ExprAggrMap;
class ExprAggrStruct;
class ExprRefPathContext;
class ExprRefPathId;
class ExprRefPathStatic;
class ExprRefPathStaticRooted;
class ExprSignedNumber;
class ExprUnsignedNumber;
class ExtendType;
class Field;
class FieldClaim;
class FieldCompRef;
class FieldRef;
class FunctionImportProto;
class FunctionImportType;
class FunctionPrototype;
class GlobalScope;
class NamedScope;
class PackageScope;
class ProceduralStmtAssignment;
class ProceduralStmtBody;
class ProceduralStmtBreak;
class ProceduralStmtContinue;
class ProceduralStmtDataDeclaration;
class ProceduralStmtExpr;
class ProceduralStmtFunctionCall;
class ProceduralStmtIfElse;
class ActivityActionHandleTraversal;
class ActivityActionTypeTraversal;
class ProceduralStmtRepeatWhile;
class ActivityForeach;
class ActivityIfElse;
class ProceduralStmtWhile;
class ActivityMatch;
class ActivityRepeatCount;
class ActivityRepeatWhile;
class ActivityReplicate;
class ActivitySelect;
class SymbolScope;
class ActivitySuper;
class ConstraintBlock;
class ConstraintStmtForall;
class ConstraintStmtForeach;
class ConstraintStmtImplication;
class TypeScope;
class ExprRefPathStaticFunc;
class ExprRefPathSuper;
class Action;
class ActivityDecl;
class ProceduralStmtSymbolBodyScope;
class ConstraintSymbolScope;
class ActivityLabeledScope;
class RootSymbolScope;
class Struct;
class SymbolEnumScope;
class SymbolExtendScope;
class ExecScope;
class SymbolFunctionScope;
class SymbolTypeScope;
class Component;
class ProceduralStmtRepeat;
class ActivityParallel;
class ActivitySchedule;
class ExecBlock;
class ActivitySequence;
class ProceduralStmtForeach;

class IVisitor {
public:
    virtual ~IVisitor() { }
    
    virtual void visitExprAggrMapElem(IExprAggrMapElem *i) = 0;
    
    virtual void visitTemplateParamDeclList(ITemplateParamDeclList *i) = 0;
    
    virtual void visitExprAggrStructElem(IExprAggrStructElem *i) = 0;
    
    virtual void visitTemplateParamValue(ITemplateParamValue *i) = 0;
    
    virtual void visitTemplateParamValueList(ITemplateParamValueList *i) = 0;
    
    virtual void visitActivityJoinSpec(IActivityJoinSpec *i) = 0;
    
    virtual void visitRefExpr(IRefExpr *i) = 0;
    
    virtual void visitActivityMatchChoice(IActivityMatchChoice *i) = 0;
    
    virtual void visitScopeChild(IScopeChild *i) = 0;
    
    virtual void visitActivitySelectBranch(IActivitySelectBranch *i) = 0;
    
    virtual void visitSymbolRefPath(ISymbolRefPath *i) = 0;
    
    virtual void visitExecTargetTemplateParam(IExecTargetTemplateParam *i) = 0;
    
    virtual void visitExpr(IExpr *i) = 0;
    
    virtual void visitAssocData(IAssocData *i) = 0;
    
    virtual void visitSymbolImportSpec(ISymbolImportSpec *i) = 0;
    
    virtual void visitPyImportFromStmt(IPyImportFromStmt *i) = 0;
    
    virtual void visitActivityJoinSpecBranch(IActivityJoinSpecBranch *i) = 0;
    
    virtual void visitActivityJoinSpecFirst(IActivityJoinSpecFirst *i) = 0;
    
    virtual void visitActivityJoinSpecNone(IActivityJoinSpecNone *i) = 0;
    
    virtual void visitActivityJoinSpecSelect(IActivityJoinSpecSelect *i) = 0;
    
    virtual void visitPyImportStmt(IPyImportStmt *i) = 0;
    
    virtual void visitRefExprScopeIndex(IRefExprScopeIndex *i) = 0;
    
    virtual void visitRefExprTypeScopeContext(IRefExprTypeScopeContext *i) = 0;
    
    virtual void visitRefExprTypeScopeGlobal(IRefExprTypeScopeGlobal *i) = 0;
    
    virtual void visitScope(IScope *i) = 0;
    
    virtual void visitScopeChildRef(IScopeChildRef *i) = 0;
    
    virtual void visitSymbolChild(ISymbolChild *i) = 0;
    
    virtual void visitActivitySchedulingConstraint(IActivitySchedulingConstraint *i) = 0;
    
    virtual void visitActivityStmt(IActivityStmt *i) = 0;
    
    virtual void visitSymbolScopeRef(ISymbolScopeRef *i) = 0;
    
    virtual void visitTemplateParamDecl(ITemplateParamDecl *i) = 0;
    
    virtual void visitConstraintStmt(IConstraintStmt *i) = 0;
    
    virtual void visitTemplateParamExprValue(ITemplateParamExprValue *i) = 0;
    
    virtual void visitTemplateParamTypeValue(ITemplateParamTypeValue *i) = 0;
    
    virtual void visitTypeIdentifier(ITypeIdentifier *i) = 0;
    
    virtual void visitTypeIdentifierElem(ITypeIdentifierElem *i) = 0;
    
    virtual void visitDataType(IDataType *i) = 0;
    
    virtual void visitExecStmt(IExecStmt *i) = 0;
    
    virtual void visitExecTargetTemplateBlock(IExecTargetTemplateBlock *i) = 0;
    
    virtual void visitExprAggrLiteral(IExprAggrLiteral *i) = 0;
    
    virtual void visitExprBin(IExprBin *i) = 0;
    
    virtual void visitExprBitSlice(IExprBitSlice *i) = 0;
    
    virtual void visitExprBool(IExprBool *i) = 0;
    
    virtual void visitExprCast(IExprCast *i) = 0;
    
    virtual void visitExprCompileHas(IExprCompileHas *i) = 0;
    
    virtual void visitExprCond(IExprCond *i) = 0;
    
    virtual void visitExprDomainOpenRangeList(IExprDomainOpenRangeList *i) = 0;
    
    virtual void visitExprDomainOpenRangeValue(IExprDomainOpenRangeValue *i) = 0;
    
    virtual void visitExprHierarchicalId(IExprHierarchicalId *i) = 0;
    
    virtual void visitExprId(IExprId *i) = 0;
    
    virtual void visitExprIn(IExprIn *i) = 0;
    
    virtual void visitExprListLiteral(IExprListLiteral *i) = 0;
    
    virtual void visitExprMemberPathElem(IExprMemberPathElem *i) = 0;
    
    virtual void visitExprNull(IExprNull *i) = 0;
    
    virtual void visitExprNumber(IExprNumber *i) = 0;
    
    virtual void visitExprOpenRangeList(IExprOpenRangeList *i) = 0;
    
    virtual void visitExprOpenRangeValue(IExprOpenRangeValue *i) = 0;
    
    virtual void visitExprRefPath(IExprRefPath *i) = 0;
    
    virtual void visitExprRefPathElem(IExprRefPathElem *i) = 0;
    
    virtual void visitExprStaticRefPath(IExprStaticRefPath *i) = 0;
    
    virtual void visitExprString(IExprString *i) = 0;
    
    virtual void visitExprStructLiteral(IExprStructLiteral *i) = 0;
    
    virtual void visitExprStructLiteralItem(IExprStructLiteralItem *i) = 0;
    
    virtual void visitExprSubscript(IExprSubscript *i) = 0;
    
    virtual void visitExprUnary(IExprUnary *i) = 0;
    
    virtual void visitExtendEnum(IExtendEnum *i) = 0;
    
    virtual void visitFunctionDefinition(IFunctionDefinition *i) = 0;
    
    virtual void visitFunctionImport(IFunctionImport *i) = 0;
    
    virtual void visitFunctionParamDecl(IFunctionParamDecl *i) = 0;
    
    virtual void visitMethodParameterList(IMethodParameterList *i) = 0;
    
    virtual void visitNamedScopeChild(INamedScopeChild *i) = 0;
    
    virtual void visitPackageImportStmt(IPackageImportStmt *i) = 0;
    
    virtual void visitProceduralStmtIfClause(IProceduralStmtIfClause *i) = 0;
    
    virtual void visitProceduralStmtMatch(IProceduralStmtMatch *i) = 0;
    
    virtual void visitProceduralStmtMatchChoice(IProceduralStmtMatchChoice *i) = 0;
    
    virtual void visitActivityBindStmt(IActivityBindStmt *i) = 0;
    
    virtual void visitActivityConstraint(IActivityConstraint *i) = 0;
    
    virtual void visitProceduralStmtReturn(IProceduralStmtReturn *i) = 0;
    
    virtual void visitProceduralStmtYield(IProceduralStmtYield *i) = 0;
    
    virtual void visitActivityLabeledStmt(IActivityLabeledStmt *i) = 0;
    
    virtual void visitSymbolChildrenScope(ISymbolChildrenScope *i) = 0;
    
    virtual void visitTemplateCategoryTypeParamDecl(ITemplateCategoryTypeParamDecl *i) = 0;
    
    virtual void visitTemplateGenericTypeParamDecl(ITemplateGenericTypeParamDecl *i) = 0;
    
    virtual void visitConstraintScope(IConstraintScope *i) = 0;
    
    virtual void visitConstraintStmtDefault(IConstraintStmtDefault *i) = 0;
    
    virtual void visitConstraintStmtDefaultDisable(IConstraintStmtDefaultDisable *i) = 0;
    
    virtual void visitConstraintStmtExpr(IConstraintStmtExpr *i) = 0;
    
    virtual void visitConstraintStmtField(IConstraintStmtField *i) = 0;
    
    virtual void visitTemplateValueParamDecl(ITemplateValueParamDecl *i) = 0;
    
    virtual void visitConstraintStmtIf(IConstraintStmtIf *i) = 0;
    
    virtual void visitConstraintStmtUnique(IConstraintStmtUnique *i) = 0;
    
    virtual void visitDataTypeBool(IDataTypeBool *i) = 0;
    
    virtual void visitDataTypeChandle(IDataTypeChandle *i) = 0;
    
    virtual void visitDataTypeEnum(IDataTypeEnum *i) = 0;
    
    virtual void visitDataTypeInt(IDataTypeInt *i) = 0;
    
    virtual void visitDataTypePyObj(IDataTypePyObj *i) = 0;
    
    virtual void visitDataTypeRef(IDataTypeRef *i) = 0;
    
    virtual void visitDataTypeString(IDataTypeString *i) = 0;
    
    virtual void visitDataTypeUserDefined(IDataTypeUserDefined *i) = 0;
    
    virtual void visitEnumDecl(IEnumDecl *i) = 0;
    
    virtual void visitEnumItem(IEnumItem *i) = 0;
    
    virtual void visitExprAggrEmpty(IExprAggrEmpty *i) = 0;
    
    virtual void visitExprAggrList(IExprAggrList *i) = 0;
    
    virtual void visitExprAggrMap(IExprAggrMap *i) = 0;
    
    virtual void visitExprAggrStruct(IExprAggrStruct *i) = 0;
    
    virtual void visitExprRefPathContext(IExprRefPathContext *i) = 0;
    
    virtual void visitExprRefPathId(IExprRefPathId *i) = 0;
    
    virtual void visitExprRefPathStatic(IExprRefPathStatic *i) = 0;
    
    virtual void visitExprRefPathStaticRooted(IExprRefPathStaticRooted *i) = 0;
    
    virtual void visitExprSignedNumber(IExprSignedNumber *i) = 0;
    
    virtual void visitExprUnsignedNumber(IExprUnsignedNumber *i) = 0;
    
    virtual void visitExtendType(IExtendType *i) = 0;
    
    virtual void visitField(IField *i) = 0;
    
    virtual void visitFieldClaim(IFieldClaim *i) = 0;
    
    virtual void visitFieldCompRef(IFieldCompRef *i) = 0;
    
    virtual void visitFieldRef(IFieldRef *i) = 0;
    
    virtual void visitFunctionImportProto(IFunctionImportProto *i) = 0;
    
    virtual void visitFunctionImportType(IFunctionImportType *i) = 0;
    
    virtual void visitFunctionPrototype(IFunctionPrototype *i) = 0;
    
    virtual void visitGlobalScope(IGlobalScope *i) = 0;
    
    virtual void visitNamedScope(INamedScope *i) = 0;
    
    virtual void visitPackageScope(IPackageScope *i) = 0;
    
    virtual void visitProceduralStmtAssignment(IProceduralStmtAssignment *i) = 0;
    
    virtual void visitProceduralStmtBody(IProceduralStmtBody *i) = 0;
    
    virtual void visitProceduralStmtBreak(IProceduralStmtBreak *i) = 0;
    
    virtual void visitProceduralStmtContinue(IProceduralStmtContinue *i) = 0;
    
    virtual void visitProceduralStmtDataDeclaration(IProceduralStmtDataDeclaration *i) = 0;
    
    virtual void visitProceduralStmtExpr(IProceduralStmtExpr *i) = 0;
    
    virtual void visitProceduralStmtFunctionCall(IProceduralStmtFunctionCall *i) = 0;
    
    virtual void visitProceduralStmtIfElse(IProceduralStmtIfElse *i) = 0;
    
    virtual void visitActivityActionHandleTraversal(IActivityActionHandleTraversal *i) = 0;
    
    virtual void visitActivityActionTypeTraversal(IActivityActionTypeTraversal *i) = 0;
    
    virtual void visitProceduralStmtRepeatWhile(IProceduralStmtRepeatWhile *i) = 0;
    
    virtual void visitActivityForeach(IActivityForeach *i) = 0;
    
    virtual void visitActivityIfElse(IActivityIfElse *i) = 0;
    
    virtual void visitProceduralStmtWhile(IProceduralStmtWhile *i) = 0;
    
    virtual void visitActivityMatch(IActivityMatch *i) = 0;
    
    virtual void visitActivityRepeatCount(IActivityRepeatCount *i) = 0;
    
    virtual void visitActivityRepeatWhile(IActivityRepeatWhile *i) = 0;
    
    virtual void visitActivityReplicate(IActivityReplicate *i) = 0;
    
    virtual void visitActivitySelect(IActivitySelect *i) = 0;
    
    virtual void visitSymbolScope(ISymbolScope *i) = 0;
    
    virtual void visitActivitySuper(IActivitySuper *i) = 0;
    
    virtual void visitConstraintBlock(IConstraintBlock *i) = 0;
    
    virtual void visitConstraintStmtForall(IConstraintStmtForall *i) = 0;
    
    virtual void visitConstraintStmtForeach(IConstraintStmtForeach *i) = 0;
    
    virtual void visitConstraintStmtImplication(IConstraintStmtImplication *i) = 0;
    
    virtual void visitTypeScope(ITypeScope *i) = 0;
    
    virtual void visitExprRefPathStaticFunc(IExprRefPathStaticFunc *i) = 0;
    
    virtual void visitExprRefPathSuper(IExprRefPathSuper *i) = 0;
    
    virtual void visitAction(IAction *i) = 0;
    
    virtual void visitActivityDecl(IActivityDecl *i) = 0;
    
    virtual void visitProceduralStmtSymbolBodyScope(IProceduralStmtSymbolBodyScope *i) = 0;
    
    virtual void visitConstraintSymbolScope(IConstraintSymbolScope *i) = 0;
    
    virtual void visitActivityLabeledScope(IActivityLabeledScope *i) = 0;
    
    virtual void visitRootSymbolScope(IRootSymbolScope *i) = 0;
    
    virtual void visitStruct(IStruct *i) = 0;
    
    virtual void visitSymbolEnumScope(ISymbolEnumScope *i) = 0;
    
    virtual void visitSymbolExtendScope(ISymbolExtendScope *i) = 0;
    
    virtual void visitExecScope(IExecScope *i) = 0;
    
    virtual void visitSymbolFunctionScope(ISymbolFunctionScope *i) = 0;
    
    virtual void visitSymbolTypeScope(ISymbolTypeScope *i) = 0;
    
    virtual void visitComponent(IComponent *i) = 0;
    
    virtual void visitProceduralStmtRepeat(IProceduralStmtRepeat *i) = 0;
    
    virtual void visitActivityParallel(IActivityParallel *i) = 0;
    
    virtual void visitActivitySchedule(IActivitySchedule *i) = 0;
    
    virtual void visitExecBlock(IExecBlock *i) = 0;
    
    virtual void visitActivitySequence(IActivitySequence *i) = 0;
    
    virtual void visitProceduralStmtForeach(IProceduralStmtForeach *i) = 0;
    
};

} // namespace zsp
} // namespace ast

