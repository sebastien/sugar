" Vim syntax file
" Language:   Sugar (http://www.ivy.fr/sugar)
" Maintainer: Sébastien Pierre <sebastien@type-z.org>
" Created:    2007-04-03
" Updated:    2007-04-16

syn match   sugarComment        "^\s*#.*$" contains=sugarCommentAnn
syn match   sugarCommentAnn     /\v(TODO|NOTE|FIXME|SEE|WARNING|EOF)/ contained
syn match   sugarDocumentation  "^\s*|.*$" contains=sugarDocRef,sugarDocCode,sugarDocExample skipwhite
syn match   sugarDocRef         /@[a-zA-Z_][a-zA-Z0-9_]*/ contained
syn match   sugarDocCode        /\v'[^']+'*/ contained
syn match   sugarDocExample     /\v\>\s+.*/ contained

syn match   sugarDeclaration    /\v\@(class|shared|property|group|end)/ nextgroup=sugarDeclName skipwhite
syn match   sugarFunction       /\v\@(function|constructor|method|operation)/ nextgroup=sugarFunctionName skipwhite
syn match   sugarConstructor    /\v\@(constructor)/ nextgroup=sugarFunctionArgs skipwhite
syn match   sugarFunctionName   /\<[a-zA-Z_][a-zA-Z0-9_]*\>/  nextgroup=sugarFunctionArgs contained skipwhite
syn match   sugarFunctionArgs   ".*$" contained contains=sugarDeclName
syn match   sugarMeta           /\v\@(module|requires|version|authors|target)/ nextgroup=sugarMetaRest skipwhite
syn match   sugarAnnotation     /\v\@(as|when|pre|post|always)/ nextgroup=sugarMetaRest skipwhite
syn match   sugarMetaRest       /\v.+/ contained
syn region  sugarDict           start=+{+ end=+}+ contains=sugarPair,sugarString
syn region  sugarArray          start=+\[+ end=+\]+
syn match   sugarPair           /\<[a-zA-Z_][a-zA-Z0-9_]*\s*\:/ contained

syn keyword sugarControl        for when while match otherwise end
syn match   sugarComputation    /\v(\+|\-|\/|\^|\%)/ 
syn match   sugarOperator       /\v(is|has|\-\>|\.\.|\:\:|\=)/ 
syn match   sugarLogic          /\v(and|or|not|\!\=|\=\=|\<|\>|\>\=|\<\=)/ 
syn match   sugarInteger        /[0-9]+/
syn match   sugarFloat          /[0-9]+.[0-9]+/
syn keyword sugarValues         Undefined None Any True False
syn match   sugarName           /\<[a-zA-Z_][a-zA-Z0-9_]*\>/ 
syn match   sugarDeclName       /[a-zA-Z_][a-zA-Z0-9_]*/  nextgroup=sugarDeclType contained
syn match   sugarDeclType       /:[a-zA-Z_][a-zA-Z0-9_]*/ nextgroup=sugarDeclType contained
syn match   sugarConstant       /\<[A-Z][A-Z0-9_]\+\>/ 

syn keyword sugarAllocation     var nextgroup=sugarDeclName skipwhite
syn keyword sugarStatement      return new self super

syn region  sugarString     start=+'+ skip=+\\\\\|\\'\|\\$+ excludenl end=+'+ end=+$+ keepend
syn region  sugarString     start=+"+ skip=+\\\\\|\\"\|\\$+ excludenl end=+"+ end=+$+ keepend


hi def link sugarComment        Comment
hi def link sugarCommentAnn     Todo
hi def link sugarDocumentation  Special
hi def link sugarDocRef         Identifier
hi def link sugarDocCode        String
hi def link sugarDocExample     Statement
hi def link sugarDeclaration    Statement
hi def link sugarConstructor    Statement
hi def link sugarFunction       Statement
hi def link sugarFunctionName   Identifier
hi def link sugarFunctionArgs   Identifier
hi def link sugarDeclName       Identifier
hi def link sugarDeclType       Type
hi def link sugarName           Normal
hi def link sugarConstant       Identifier
hi def link sugarStructure      Function
hi def link sugarMeta           Special
hi def link sugarAnnotation     Special
hi def link sugarMetaRest       Statement
hi def link sugarDict           Special
hi def link sugarArray          Special
hi def link sugarPair           Identifier
hi def link sugarControl        Conditional
hi def link sugarOperator       Conditional
hi def link sugarComputation    Special
hi def link sugarLogic          Special
hi def link sugarAllocation     Statement
hi def link sugarStatement      Statement
hi def link sugarString         String
hi def link sugarInteger        Number
hi def link sugarFloat          Float
hi def link sugarValues         String

set textwidth=80
set noet
set ts=4
set sw=4

" This does not work, I don't know why :/
let b:current_syntax = "sugar"

" EOF
