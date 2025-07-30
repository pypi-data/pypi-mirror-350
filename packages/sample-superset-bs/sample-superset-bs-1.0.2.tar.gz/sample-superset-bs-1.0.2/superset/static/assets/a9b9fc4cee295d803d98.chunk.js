(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1285],{9063:(e,t,n)=>{var i=n(55765);e.exports=function(e,t){return t="function"==typeof t?t:void 0,e&&e.length?i(e,void 0,t):[]}},14693:(e,t,n)=>{"use strict";n.d(t,{QD:()=>x.Q,Ay:()=>$});var i=n(9063),a=n.n(i),r=n(96540),o=n(98250),l=n(96453),d=n(19129),s=n(62952),c=n(78518),h=n(67073),p=n(2445);const u=l.I4.div`
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,g=({text:e,header:t})=>{const n=(0,s.A)(e);return(0,p.FD)(p.FK,{children:[t&&(0,p.Y)(u,{children:t}),n.map((e=>(0,p.Y)("div",{children:e},e)))]})},m=16,b={dashboards:0,table:1,sql:2,rows:3,tags:4,description:5,owner:6,lastModified:7},f=l.I4.div`
  ${({theme:e,count:t})=>`\n    display: flex;\n    align-items: center;\n    padding: 8px 12px;\n    background-color: ${e.colors.grayscale.light4};\n    color: ${e.colors.grayscale.base};\n    font-size: ${e.typography.sizes.s}px;\n    min-width: ${24+32*t-m}px;\n    border-radius: ${e.borderRadius}px;\n    line-height: 1;\n  `}
`,y=l.I4.div`
  ${({theme:e,collapsed:t,last:n,onClick:i})=>`\n    display: flex;\n    align-items: center;\n    max-width: ${174+(n?0:m)}px;\n    min-width: ${t?16+(n?0:m):94+(n?0:m)}px;\n    padding-right: ${n?0:m}px;\n    cursor: ${i?"pointer":"default"};\n    & .metadata-icon {\n      color: ${i&&t?e.colors.primary.base:e.colors.grayscale.base};\n      padding-right: ${t?0:8}px;\n      & .anticon {\n        line-height: 0;\n      }\n    }\n    & .metadata-text {\n      min-width: 70px;\n      overflow: hidden;\n      text-overflow: ${t?"unset":"ellipsis"};\n      white-space: nowrap;\n      text-decoration: ${i?"underline":"none"};\n      line-height: 1.4;\n    }\n  `}
`,v=l.I4.div`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,w=({barWidth:e,contentType:t,collapsed:n,last:i=!1,tooltipPlacement:a})=>{const{icon:o,title:l,tooltip:s=l}=(e=>{const{type:t}=e;switch(t){case x.Q.Dashboards:return{icon:h.F.FundProjectionScreenOutlined,title:e.title,tooltip:e.description?(0,p.Y)("div",{children:(0,p.Y)(g,{header:e.title,text:e.description})}):void 0};case x.Q.Description:return{icon:h.F.BookOutlined,title:e.value};case x.Q.LastModified:return{icon:h.F.EditOutlined,title:e.value,tooltip:(0,p.FD)("div",{children:[(0,p.Y)(g,{header:(0,c.t)("Last modified"),text:e.value}),(0,p.Y)(g,{header:(0,c.t)("Modified by"),text:e.modifiedBy})]})};case x.Q.Owner:return{icon:h.F.UserOutlined,title:e.createdBy,tooltip:(0,p.FD)("div",{children:[(0,p.Y)(g,{header:(0,c.t)("Created by"),text:e.createdBy}),!!e.owners&&(0,p.Y)(g,{header:(0,c.t)("Owners"),text:e.owners}),(0,p.Y)(g,{header:(0,c.t)("Created on"),text:e.createdOn})]})};case x.Q.Rows:return{icon:h.F.InsertRowBelowOutlined,title:e.title,tooltip:e.title};case x.Q.Sql:return{icon:h.F.ConsoleSqlOutlined,title:e.title,tooltip:e.title};case x.Q.Table:return{icon:h.F.InsertRowAboveOutlined,title:e.title,tooltip:e.title};case x.Q.Tags:return{icon:h.F.TagsOutlined,title:e.values.join(", "),tooltip:(0,p.Y)("div",{children:(0,p.Y)(g,{header:(0,c.t)("Tags"),text:e.values})})};default:throw Error(`Invalid type provided: ${t}`)}})(t),[u,m]=(0,r.useState)(!1),b=(0,r.useRef)(null),f=o,{type:w,onClick:$}=t;(0,r.useEffect)((()=>{m(!!b.current&&b.current.scrollWidth>b.current.clientWidth)}),[e,m,t]);const S=(0,p.FD)(y,{collapsed:n,last:i,onClick:$?()=>$(w):void 0,role:$?"button":void 0,children:[(0,p.Y)(f,{iconSize:"l",className:"metadata-icon"}),!n&&(0,p.Y)("span",{ref:b,className:"metadata-text",children:l})]});return u||n||s&&s!==l?(0,p.Y)(d.m_,{placement:a,title:(0,p.Y)(v,{children:s}),children:S}):S};var x=n(70175);const $=({items:e,tooltipPlacement:t="top"})=>{const[n,i]=(0,r.useState)(),[l,d]=(0,r.useState)(!1),s=a()(e,((e,t)=>e.type===t.type)).sort(((e,t)=>b[e.type]-b[t.type])),c=s.length;if(c<2)throw Error("The minimum number of items for the metadata bar is 2.");if(c>6)throw Error("The maximum number of items for the metadata bar is 6.");const h=(0,r.useCallback)((e=>{const t=110*c-m;i(e),d(Boolean(e&&e<t))}),[c]),{ref:u}=(0,o.uZ)({onResize:h});return(0,p.Y)(f,{ref:u,count:c,"data-test":"metadata-bar",children:s.map(((e,i)=>(0,p.Y)(w,{barWidth:n,contentType:e,collapsed:l,last:i===c-1,tooltipPlacement:t},i)))})}},20473:(e,t,n)=>{"use strict";n.d(t,{A:()=>v});var i=n(96540),a=n(58561),r=n.n(a),o=n(85861),l=n(49756),d=n(40563),s=n(96453),c=n(35742),h=n(78518),p=n(36255),u=n(85955),g=n(46920),m=n(97567),b=n(2445);const f=s.I4.div`
  .ant-select-dropdown {
    max-height: ${({theme:e})=>40*e.gridUnit}px;
  }
  .tag-input {
    margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  }
`;var y;!function(e){e.Chart="chart",e.Dashboard="dashboard",e.SavedQuery="query"}(y||(y={}));const v=({show:e,onHide:t,editTag:n,refreshData:a,addSuccessToast:s,addDangerToast:v,clearOnHide:w=!1})=>{const[x,$]=(0,i.useState)([]),[S,Y]=(0,i.useState)([]),[k,T]=(0,i.useState)([]),[A,C]=(0,i.useState)(""),[D,I]=(0,i.useState)(""),z=!!n,E=z?"Edit Tag":"Create Tag",F=()=>{C(""),I(""),$([]),Y([]),T([])};(0,i.useEffect)((()=>{const e={[y.Dashboard]:[],[y.Chart]:[],[y.SavedQuery]:[]},t=({id:t,name:n,type:i})=>{const a=e[i];a&&a.push({value:t,label:n,key:t})};$([]),Y([]),T([]),z&&((0,m.Ik)({tagIds:[n.id],types:null},(n=>{n.forEach(t),$(e[y.Dashboard]),Y(e[y.Chart]),T(e[y.SavedQuery])}),(e=>{v("Error Fetching Tagged Objects")})),C(n.name),I(n.description))}),[n]);const O=async(e,t,n,i,a,o,l)=>{const d=r().encode({columns:i,filters:[{col:a,opr:"ct",value:e}],page:t,order_column:o}),{json:s}=await c.A.get({endpoint:`/api/v1/${l}/?q=${d}`}),{result:h,count:p}=s;return{data:h.map((e=>({value:e.id,label:e[a]}))),totalCount:p}},P=(e,t)=>{e===y.Dashboard?$(t):e===y.Chart?Y(t):e===y.SavedQuery&&T(t)};return(0,b.Y)(o.Ay,{title:E,onHide:()=>{w&&F(),t()},show:e,footer:(0,b.FD)("div",{children:[(0,b.Y)(g.A,{"data-test":"modal-save-dashboard-button",buttonStyle:"secondary",onClick:t,children:(0,h.t)("Cancel")}),(0,b.Y)(g.A,{"data-test":"modal-save-dashboard-button",buttonStyle:"primary",onClick:()=>{const e=x.map((e=>["dashboard",e.value])),i=S.map((e=>["chart",e.value])),r=k.map((e=>["query",e.value]));z?c.A.put({endpoint:`/api/v1/tag/${n.id}`,jsonPayload:{description:D,name:A,objects_to_tag:[...e,...i,...r]}}).then((({json:e={}})=>{a(),F(),s((0,h.t)("Tag updated")),t()})).catch((e=>{v(e.message||"Error Updating Tag")})):c.A.post({endpoint:"/api/v1/tag/",jsonPayload:{description:D,name:A,objects_to_tag:[...e,...i,...r]}}).then((({json:e={}})=>{a(),F(),s((0,h.t)("Tag created")),t()})).catch((e=>v(e.message||"Error Creating Tag")))},children:(0,h.t)("Save")})]}),children:(0,b.FD)(f,{children:[(0,b.Y)(d.lR,{children:(0,h.t)("Tag name")}),(0,b.Y)(p.A,{className:"tag-input",onChange:e=>C(e.target.value),placeholder:(0,h.t)("Name of your tag"),value:A}),(0,b.Y)(d.lR,{children:(0,h.t)("Description")}),(0,b.Y)(p.A,{className:"tag-input",onChange:e=>I(e.target.value),placeholder:(0,h.t)("Add description of your tag"),value:D}),(0,b.Y)(u.c,{}),(0,b.Y)(l.A,{className:"tag-input",ariaLabel:(0,h.t)("Select dashboards"),mode:"multiple",name:"dashboards",value:x,options:async(e,t,n)=>O(e,t,0,["id","dashboard_title"],"dashboard_title","dashboard_title","dashboard"),onChange:e=>P(y.Dashboard,e),header:(0,b.Y)(d.lR,{children:(0,h.t)("Dashboards")}),allowClear:!0}),(0,b.Y)(l.A,{className:"tag-input",ariaLabel:(0,h.t)("Select charts"),mode:"multiple",name:"charts",value:S,options:async(e,t,n)=>O(e,t,0,["id","slice_name"],"slice_name","slice_name","chart"),onChange:e=>P(y.Chart,e),header:(0,b.Y)(d.lR,{children:(0,h.t)("Charts")}),allowClear:!0}),(0,b.Y)(l.A,{className:"tag-input",ariaLabel:(0,h.t)("Select saved queries"),mode:"multiple",name:"savedQueries",value:k,options:async(e,t,n)=>O(e,t,0,["id","label"],"label","label","saved_query"),onChange:e=>P(y.SavedQuery,e),header:(0,b.Y)(d.lR,{children:(0,h.t)("Saved queries")}),allowClear:!0})]})})}},25143:(e,t,n)=>{"use strict";n.d(t,{S:()=>i.A,v:()=>a.A});var i=n(46740),a=n(16707)},45418:(e,t,n)=>{"use strict";n.d(t,{A:()=>b});var i=n(96540),a=n(46942),r=n.n(a),o=n(22553),l=n(13147),d=n(6311),s=n(1051),c=n(96424),h=n(14277);const p=e=>{const{componentCls:t}=e;return{[t]:{"&-horizontal":{[`&${t}`]:{"&-sm":{marginBlock:e.marginXS},"&-md":{marginBlock:e.margin}}}}}},u=e=>{const{componentCls:t,sizePaddingEdgeHorizontal:n,colorSplit:i,lineWidth:a,textPaddingInline:r,orientationMargin:o,verticalMarginInline:l}=e;return{[t]:Object.assign(Object.assign({},(0,s.dF)(e)),{borderBlockStart:`${(0,d.unit)(a)} solid ${i}`,"&-vertical":{position:"relative",top:"-0.06em",display:"inline-block",height:"0.9em",marginInline:l,marginBlock:0,verticalAlign:"middle",borderTop:0,borderInlineStart:`${(0,d.unit)(a)} solid ${i}`},"&-horizontal":{display:"flex",clear:"both",width:"100%",minWidth:"100%",margin:`${(0,d.unit)(e.marginLG)} 0`},[`&-horizontal${t}-with-text`]:{display:"flex",alignItems:"center",margin:`${(0,d.unit)(e.dividerHorizontalWithTextGutterMargin)} 0`,color:e.colorTextHeading,fontWeight:500,fontSize:e.fontSizeLG,whiteSpace:"nowrap",textAlign:"center",borderBlockStart:`0 ${i}`,"&::before, &::after":{position:"relative",width:"50%",borderBlockStart:`${(0,d.unit)(a)} solid transparent`,borderBlockStartColor:"inherit",borderBlockEnd:0,transform:"translateY(50%)",content:"''"}},[`&-horizontal${t}-with-text-start`]:{"&::before":{width:`calc(${o} * 100%)`},"&::after":{width:`calc(100% - ${o} * 100%)`}},[`&-horizontal${t}-with-text-end`]:{"&::before":{width:`calc(100% - ${o} * 100%)`},"&::after":{width:`calc(${o} * 100%)`}},[`${t}-inner-text`]:{display:"inline-block",paddingBlock:0,paddingInline:r},"&-dashed":{background:"none",borderColor:i,borderStyle:"dashed",borderWidth:`${(0,d.unit)(a)} 0 0`},[`&-horizontal${t}-with-text${t}-dashed`]:{"&::before, &::after":{borderStyle:"dashed none none"}},[`&-vertical${t}-dashed`]:{borderInlineStartWidth:a,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},"&-dotted":{background:"none",borderColor:i,borderStyle:"dotted",borderWidth:`${(0,d.unit)(a)} 0 0`},[`&-horizontal${t}-with-text${t}-dotted`]:{"&::before, &::after":{borderStyle:"dotted none none"}},[`&-vertical${t}-dotted`]:{borderInlineStartWidth:a,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},[`&-plain${t}-with-text`]:{color:e.colorText,fontWeight:"normal",fontSize:e.fontSize},[`&-horizontal${t}-with-text-start${t}-no-default-orientation-margin-start`]:{"&::before":{width:0},"&::after":{width:"100%"},[`${t}-inner-text`]:{paddingInlineStart:n}},[`&-horizontal${t}-with-text-end${t}-no-default-orientation-margin-end`]:{"&::before":{width:"100%"},"&::after":{width:0},[`${t}-inner-text`]:{paddingInlineEnd:n}}})}},g=(0,c.OF)("Divider",(e=>{const t=(0,h.mergeToken)(e,{dividerHorizontalWithTextGutterMargin:e.margin,sizePaddingEdgeHorizontal:0});return[u(t),p(t)]}),(e=>({textPaddingInline:"1em",orientationMargin:.05,verticalMarginInline:e.marginXS})),{unitless:{orientationMargin:!0}});const m={small:"sm",middle:"md"},b=e=>{const{getPrefixCls:t,direction:n,className:a,style:d}=(0,o.TP)("divider"),{prefixCls:s,type:c="horizontal",orientation:h="center",orientationMargin:p,className:u,rootClassName:b,children:f,dashed:y,variant:v="solid",plain:w,style:x,size:$}=e,S=function(e,t){var n={};for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&t.indexOf(i)<0&&(n[i]=e[i]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var a=0;for(i=Object.getOwnPropertySymbols(e);a<i.length;a++)t.indexOf(i[a])<0&&Object.prototype.propertyIsEnumerable.call(e,i[a])&&(n[i[a]]=e[i[a]])}return n}(e,["prefixCls","type","orientation","orientationMargin","className","rootClassName","children","dashed","variant","plain","style","size"]),Y=t("divider",s),[k,T,A]=g(Y),C=(0,l.A)($),D=m[C],I=!!f,z=i.useMemo((()=>"left"===h?"rtl"===n?"end":"start":"right"===h?"rtl"===n?"start":"end":h),[n,h]),E="start"===z&&null!=p,F="end"===z&&null!=p,O=r()(Y,a,T,A,`${Y}-${c}`,{[`${Y}-with-text`]:I,[`${Y}-with-text-${z}`]:I,[`${Y}-dashed`]:!!y,[`${Y}-${v}`]:"solid"!==v,[`${Y}-plain`]:!!w,[`${Y}-rtl`]:"rtl"===n,[`${Y}-no-default-orientation-margin-start`]:E,[`${Y}-no-default-orientation-margin-end`]:F,[`${Y}-${D}`]:!!D},u,b),P=i.useMemo((()=>"number"==typeof p?p:/^\d+$/.test(p)?Number(p):p),[p]),U={marginInlineStart:E?P:void 0,marginInlineEnd:F?P:void 0};return k(i.createElement("div",Object.assign({className:O,style:Object.assign(Object.assign({},d),x)},S,{role:"separator"}),f&&"vertical"!==c&&i.createElement("span",{className:`${Y}-inner-text`,style:U},f)))}},51848:(e,t,n)=>{"use strict";n.d(t,{U:()=>x});var i=n(17437),a=n(96453),r=n(78518),o=n(93103),l=n(67073),d=n(96540),s=n(19129),c=n(98250),h=n(2445);const p=e=>i.AH`
  display: flex;
  font-size: ${e.typography.sizes.xl}px;
  font-weight: ${e.typography.weights.bold};
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  & .dynamic-title,
  & .dynamic-title-input {
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  & .dynamic-title {
    cursor: default;
  }
  & .dynamic-title-input {
    border: none;
    padding: 0;
    outline: none;

    &::placeholder {
      color: ${e.colors.grayscale.light1};
    }
  }

  & .input-sizer {
    position: absolute;
    left: -9999px;
    display: inline-block;
    white-space: pre;
  }
`,u=(0,d.memo)((({title:e,placeholder:t,onSave:n,canEdit:a,label:o})=>{const[l,u]=(0,d.useState)(!1),[g,m]=(0,d.useState)(e||""),b=(0,d.useRef)(null),[f,y]=(0,d.useState)(!1),{width:v,ref:w}=(0,c.uZ)(),{width:x,ref:$}=(0,c.uZ)({refreshMode:"debounce"});(0,d.useEffect)((()=>{m(e)}),[e]),(0,d.useEffect)((()=>{if(l&&null!=b&&b.current&&(b.current.focus(),b.current.setSelectionRange)){const{length:e}=b.current.value;b.current.setSelectionRange(e,e),b.current.scrollLeft=b.current.scrollWidth}}),[l]),(0,d.useLayoutEffect)((()=>{null!=w&&w.current&&(w.current.textContent=g||t)}),[g,t,w]),(0,d.useEffect)((()=>{b.current&&b.current.scrollWidth>b.current.clientWidth?y(!0):y(!1)}),[v,x]);const S=(0,d.useCallback)((()=>{a&&!l&&u(!0)}),[a,l]),Y=(0,d.useCallback)((()=>{if(!a)return;const t=g.trim();m(t),e!==t&&n(t),u(!1)}),[a,g,n,e]),k=(0,d.useCallback)((e=>{a&&l&&m(e.target.value)}),[a,l]),T=(0,d.useCallback)((e=>{var t;a&&"Enter"===e.key&&(e.preventDefault(),null==(t=b.current)||t.blur())}),[a]);return(0,h.FD)("div",{css:p,ref:$,children:[(0,h.Y)(s.m_,{id:"title-tooltip",title:f&&g&&!l?g:null,children:a?(0,h.Y)("input",{"data-test":"editable-title-input",className:"dynamic-title-input","aria-label":null!=o?o:(0,r.t)("Title"),ref:b,onChange:k,onBlur:Y,onClick:S,onKeyPress:T,placeholder:t,value:g,css:i.AH`
                cursor: ${l?"text":"pointer"};

                ${v&&v>0&&i.AH`
                  width: ${v+1}px;
                `}
              `}):(0,h.Y)("span",{className:"dynamic-title","aria-label":null!=o?o:(0,r.t)("Title"),ref:b,"data-test":"editable-title",children:g})}),(0,h.Y)("span",{ref:w,className:"input-sizer","aria-hidden":!0,tabIndex:-1})]})}));var g=n(58132),m=n(94704),b=n(46920);const f=e=>i.AH`
  width: ${8*e.gridUnit}px;
  height: ${8*e.gridUnit}px;
  padding: 0;
  border: 1px solid ${e.colors.primary.dark2};

  &.antd5-btn > span.anticon {
    line-height: 0;
    transition: inherit;
  }

  &:hover:not(:focus) > span.anticon {
    color: ${e.colors.primary.light1};
  }
  &:focus-visible {
    outline: 2px solid ${e.colors.primary.dark2};
  }
`,y=e=>i.AH`
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: nowrap;
  justify-content: space-between;
  background-color: ${e.colors.grayscale.light5};
  height: ${16*e.gridUnit}px;
  padding: 0 ${4*e.gridUnit}px;

  .editable-title {
    overflow: hidden;

    & > input[type='button'],
    & > span {
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      white-space: nowrap;
    }
  }

  span[role='button'] {
    display: flex;
    height: 100%;
  }

  .title-panel {
    display: flex;
    align-items: center;
    min-width: 0;
    margin-right: ${12*e.gridUnit}px;
  }

  .right-button-panel {
    display: flex;
    align-items: center;
  }
`,v=e=>i.AH`
  display: flex;
  align-items: center;
  padding-left: ${2*e.gridUnit}px;

  & .anticon-star {
    padding: 0 ${e.gridUnit}px;

    &:first-of-type {
      padding-left: 0;
    }
  }
`,w=e=>i.AH`
  margin-left: ${2*e.gridUnit}px;
`,x=({editableTitleProps:e,showTitlePanelItems:t,certificatiedBadgeProps:n,showFaveStar:i,faveStarProps:d,titlePanelAdditionalItems:s,rightPanelAdditionalItems:c,additionalActionsMenu:p,menuDropdownProps:x,showMenuDropdown:$=!0,tooltipProps:S})=>{const Y=(0,a.DP)();return(0,h.FD)("div",{css:y,className:"header-with-actions",children:[(0,h.FD)("div",{className:"title-panel",children:[(0,h.Y)(u,{...e}),t&&(0,h.FD)("div",{css:v,children:[(null==n?void 0:n.certifiedBy)&&(0,h.Y)(g.A,{...n}),i&&(0,h.Y)(m.A,{...d}),s]})]}),(0,h.FD)("div",{className:"right-button-panel",children:[c,(0,h.Y)("div",{css:w,children:$&&(0,h.Y)(o.ms,{trigger:["click"],dropdownRender:()=>p,...x,children:(0,h.Y)(b.A,{css:f,buttonStyle:"tertiary","aria-label":(0,r.t)("Menu actions trigger"),tooltip:null==S?void 0:S.text,placement:null==S?void 0:S.placement,"data-test":"actions-trigger",children:(0,h.Y)(l.F.EllipsisOutlined,{iconColor:Y.colors.primary.dark2,iconSize:"l"})})})})]})]})}},70175:(e,t,n)=>{"use strict";var i;n.d(t,{Q:()=>i}),function(e){e.Dashboards="dashboards",e.Description="description",e.LastModified="lastModified",e.Owner="owner",e.Rows="rows",e.Sql="sql",e.Table="table",e.Tags="tags"}(i||(i={}))},85955:(e,t,n)=>{"use strict";n.d(t,{c:()=>r});var i=n(45418),a=n(2445);function r(e){return(0,a.Y)(i.A,{...e})}},86014:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>A});var i=n(96540),a=n(17437),r=n(96453),o=n(78518),l=n(33231),d=n(7089),s=n(50217),c=n(25143),h=n(42319),p=n(50455),u=n(2445);const g=r.I4.div`
  text-align: left;
  border-radius: ${({theme:e})=>1*e.gridUnit}px 0;
  .table {
    table-layout: fixed;
  }
  .td {
    width: 33%;
  }
  .entity-title {
    font-family: Inter;
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
    font-weight: ${({theme:e})=>e.typography.weights.medium};
    line-height: 17px;
    letter-spacing: 0px;
    text-align: left;
    margin: ${({theme:e})=>4*e.gridUnit}px 0;
  }
`;function m({search:e="",setShowTagModal:t,objects:n}){const[i]=(0,l.pE)("id",l.hc),a=n.dashboard.length>0||n.chart.length>0||n.query.length>0,r=e=>{const t=n[e].map((t=>({[e]:(0,u.Y)("a",{href:t.url,children:t.name}),modified:d.XV.utc(t.changed_on).fromNow(),tags:t.tags,owners:t.owners})));return(0,u.Y)(s.A,{className:"table-condensed",emptyWrapperType:s.V.Small,data:t,pageSize:10,columns:[{accessor:e,Header:"Title"},{Cell:({row:{original:{tags:e=[]}}})=>(0,u.Y)(c.S,{tags:e.filter((e=>void 0!==e.type&&["TagType.custom",1].includes(e.type)&&e.id!==i)),maxTags:3}),Header:(0,o.t)("Tags"),accessor:"tags",disableSortBy:!0},{Cell:({row:{original:{owners:e=[]}}})=>(0,u.Y)(h.A,{users:e}),Header:(0,o.t)("Owners"),accessor:"owners",disableSortBy:!0,size:"xl"}]})};return(0,u.Y)(g,{children:a?(0,u.FD)(u.FK,{children:[(0,u.Y)("div",{className:"entity-title",children:(0,o.t)("Dashboards")}),r("dashboard"),(0,u.Y)("div",{className:"entity-title",children:(0,o.t)("Charts")}),r("chart"),(0,u.Y)("div",{className:"entity-title",children:(0,o.t)("Queries")}),r("query")]}):(0,u.Y)(p.p,{image:"dashboard.svg",size:"large",title:(0,o.t)("No entities have this tag currently assigned"),buttonAction:()=>t(!0),buttonText:(0,o.t)("Add tag to entities")})})}var b=n(46920),f=n(14693),y=n(51848),v=n(20473),w=n(5261),x=n(97567),$=n(17444),S=n(25106);const Y=e=>a.AH`
  display: flex;
  align-items: center;
  margin-left: ${e.gridUnit}px;
  & > span {
    margin-right: ${3*e.gridUnit}px;
  }
`,k=r.I4.div`
  ${({theme:e})=>`\n  background-color: ${e.colors.grayscale.light4};\n  .select-control {\n    margin-left: ${4*e.gridUnit}px;\n    margin-right: ${4*e.gridUnit}px;\n    margin-bottom: ${2*e.gridUnit}px;\n  }\n  .select-control-label {\n    font-size: ${3*e.gridUnit}px;\n    color: ${e.colors.grayscale.base};\n    margin-bottom: ${1*e.gridUnit}px;\n  }\n  .entities {\n    margin: ${6*e.gridUnit}px; 0px;\n  }\n  .pagination-container {\n    background-color: transparent;\n  }\n  `}
`,T=r.I4.div`
  ${({theme:e})=>`\n  height: ${12.5*e.gridUnit}px;\n  background-color: ${e.colors.grayscale.light5};\n  margin-bottom: ${4*e.gridUnit}px;\n  .navbar-brand {\n    margin-left: ${2*e.gridUnit}px;\n    font-weight: ${e.typography.weights.bold};\n  }\n  .header {\n    font-weight: ${e.typography.weights.bold};\n    margin-right:  ${3*e.gridUnit}px;\n    text-align: left;\n    font-size: ${4.5*e.gridUnit}px;\n    padding: ${3*e.gridUnit}px;\n    display: inline-block;\n    line-height: ${9*e.gridUnit}px;\n  }\n  `};
`,A=(0,w.Ay)((function(){const[e]=(0,l.pE)("id",l.hc),[t,n]=(0,i.useState)(null),[a,r]=(0,i.useState)(!1),{addSuccessToast:d,addDangerToast:s}=(0,w.Yf)(),[c,h]=(0,i.useState)(!1),[p,g]=(0,i.useState)({dashboard:[],chart:[],query:[]}),A={title:(null==t?void 0:t.name)||"",placeholder:"testing",onSave:e=>{},canEdit:!1,label:(0,o.t)("dataset name")},C=[];if(null!=t&&t.description){const e={type:f.QD.Description,value:(null==t?void 0:t.description)||""};C.push(e)}const D={type:f.QD.Owner,createdBy:(0,S.A)(null==t?void 0:t.created_by),createdOn:(null==t?void 0:t.created_on_delta_humanized)||""};C.push(D);const I={type:f.QD.LastModified,value:(null==t?void 0:t.changed_on_delta_humanized)||"",modifiedBy:(0,S.A)(null==t?void 0:t.changed_by)};C.push(I);const z=()=>{h(!0),t?(0,x.Ik)({tagIds:void 0!==(null==t?void 0:t.id)?[t.id]:"",types:null},(e=>{const t={dashboard:[],chart:[],query:[]};e.forEach((function(e){const n=e.type;t[n].push(e)})),g(t),h(!1)}),(e=>{s("Error Fetching Tagged Objects"),h(!1)})):s("Error tag object is not referenced!")},E=e=>{(0,x.FA)(e,(e=>{n(e),h(!1)}),(e=>{s((0,o.t)("Error Fetching Tagged Objects")),h(!1)}))};return(0,i.useEffect)((()=>{e&&(h(!0),E(e))}),[e]),(0,i.useEffect)((()=>{t&&z()}),[t]),c?(0,u.Y)($.A,{}):(0,u.FD)(k,{children:[(0,u.Y)(v.A,{show:a,onHide:()=>{r(!1)},editTag:t,addSuccessToast:d,addDangerToast:s,refreshData:()=>{z(),e&&E(e)}}),(0,u.Y)(T,{children:(0,u.Y)(y.U,{additionalActionsMenu:(0,u.Y)(u.FK,{}),editableTitleProps:A,faveStarProps:{itemId:1,saveFaveStar:()=>{}},showFaveStar:!1,showTitlePanelItems:!0,titlePanelAdditionalItems:(0,u.Y)("div",{css:Y,children:(0,u.Y)(f.Ay,{items:C,tooltipPlacement:"bottom"})}),rightPanelAdditionalItems:(0,u.Y)(u.FK,{children:(0,u.FD)(b.A,{"data-test":"bulk-select-action",buttonStyle:"secondary",onClick:()=>r(!0),showMarginRight:!1,children:[(0,o.t)("Edit Tag")," "]})}),menuDropdownProps:{disabled:!0},showMenuDropdown:!1})}),(0,u.Y)("div",{className:"entities",children:(0,u.Y)(m,{search:(null==t?void 0:t.name)||"",setShowTagModal:r,objects:p})})]})}))}}]);