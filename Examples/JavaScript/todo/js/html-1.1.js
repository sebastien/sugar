var html=new Object()
html.__ce=function(name,args)
{var node=document.createElement(name)
var append=function(node,value){if(value==undefined)
{return;}
else if(typeof(value)=="string")
{node.appendChild(document.createTextNode(value))}
else if(typeof(value)=="object"&&typeof(value.nodeType)!="undefined")
{node.appendChild(value)}
else if(typeof(value)=="object"&&value instanceof Array)
{for(var j=0;j<value.length;j++)
{append(node,value[j]);}}
else
{var has_properties=false
for(var k in value){if(k=="_"||k=="_class"||k=="klass")
{node.setAttribute("class",value[k])}
else
{node.setAttribute(k,value[k])}
has_properties=true}
if(!has_properties)
{node.appendChild(document.createTextNode(""+value))}}}
for(var i=0;i<args.length;i++)
{append(node,args[i])}
return node;}
html.SUB=html.sub=function(){return html.__ce('sub',arguments)};html.SUP=html.sup=function(){return html.__ce('sup',arguments)};html.SPAN=html.span=function(){return html.__ce('span',arguments)};html.BDO=html.bdo=function(){return html.__ce('bdo',arguments)};html.BR=html.br=function(){return html.__ce('br',arguments)};html.BODY=html.body=function(){return html.__ce('body',arguments)};html.ADDRESS=html.address=function(){return html.__ce('address',arguments)};html.DIV=html.div=function(){return html.__ce('div',arguments)};html.A=html.a=function(){return html.__ce('a',arguments)};html.MAP=html.map=function(){return html.__ce('map',arguments)};html.AREA=html.area=function(){return html.__ce('area',arguments)};html.LINK=html.link=function(){return html.__ce('link',arguments)};html.IMG=html.img=function(){return html.__ce('img',arguments)};html.OBJECT=html.object=function(){return html.__ce('object',arguments)};html.PARAM=html.param=function(){return html.__ce('param',arguments)};html.HR=html.hr=function(){return html.__ce('hr',arguments)};html.P=html.p=function(){return html.__ce('p',arguments)};html.PRE=html.pre=function(){return html.__ce('pre',arguments)};html.Q=html.q=function(){return html.__ce('q',arguments)};html.BLOCKQUOTE=html.blockquote=function(){return html.__ce('blockquote',arguments)};html.INS=html.ins=function(){return html.__ce('ins',arguments)};html.DEL=html.del=function(){return html.__ce('del',arguments)};html.DL=html.dl=function(){return html.__ce('dl',arguments)};html.DT=html.dt=function(){return html.__ce('dt',arguments)};html.DD=html.dd=function(){return html.__ce('dd',arguments)};html.OL=html.ol=function(){return html.__ce('ol',arguments)};html.UL=html.ul=function(){return html.__ce('ul',arguments)};html.LI=html.li=function(){return html.__ce('li',arguments)};html.FORM=html.form=function(){return html.__ce('form',arguments)};html.LABEL=html.label=function(){return html.__ce('label',arguments)};html.INPUT=html.input=function(){return html.__ce('input',arguments)};html.SELECT=html.select=function(){return html.__ce('select',arguments)};html.OPTGROUP=html.optgroup=function(){return html.__ce('optgroup',arguments)};html.OPTION=html.option=function(){return html.__ce('option',arguments)};html.CODE=html.code=function(){return html.__ce('code',arguments)};html.TEXTAREA=html.textarea=function(){return html.__ce('textarea',arguments)};html.FIELDSET=html.fieldset=function(){return html.__ce('fieldset',arguments)};html.SMALL=html.small=function(){return html.__ce('small',arguments)};html.LEGEND=html.legend=function(){return html.__ce('legend',arguments)};html.BUTTON=html.button=function(){return html.__ce('button',arguments)};html.TABLE=html.table=function(){return html.__ce('table',arguments)};html.CAPTION=html.caption=function(){return html.__ce('caption',arguments)};html.THEAD=html.thead=function(){return html.__ce('thead',arguments)};html.TFOOT=html.tfoot=function(){return html.__ce('tfoot',arguments)};html.TBODY=html.tbody=function(){return html.__ce('tbody',arguments)};html.COLGROUP=html.colgroup=function(){return html.__ce('colgroup',arguments)};html.COL=html.col=function(){return html.__ce('col',arguments)};html.TR=html.tr=function(){return html.__ce('tr',arguments)};html.TH=html.th=function(){return html.__ce('th',arguments)};html.TD=html.td=function(){return html.__ce('td',arguments)};html.HEAD=html.head=function(){return html.__ce('head',arguments)};html.TITLE=html.title=function(){return html.__ce('title',arguments)};html.BASE=html.base=function(){return html.__ce('base',arguments)};html.META=html.meta=function(){return html.__ce('meta',arguments)};html.STYLE=html.style=function(){return html.__ce('style',arguments)};html.SCRIPT=html.script=function(){return html.__ce('script',arguments)};html.NOSCRIPT=html.noscript=function(){return html.__ce('noscript',arguments)};html.HTML=html.html=function(){return html.__ce('html',arguments)};html.IFRAME=html.iframe=function(){return html.__ce('iframe',arguments)};html.H1=html.h1=function(){return html.__ce('h1',arguments)};html.H2=html.h2=function(){return html.__ce('h2',arguments)};html.H3=html.h3=function(){return html.__ce('h3',arguments)};
