"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7745],{31641:(e,t,i)=>{i.d(t,{A:()=>m});var n=i(96453),r=i(17437),o=i(19129),l=i(67073),a=i(2445);const s=(0,n.I4)(o.m_)`
  cursor: pointer;
`,d=n.I4.span`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,c={fontSize:"12px",lineHeight:"16px"},h=n.I4.div`
  ${({theme:e})=>r.AH`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin-left: ${e.gridUnit}px;
  `}
`,p="rgba(0,0,0,0.9)";function m({tooltip:e,iconStyle:t={},placement:i="right",trigger:r="hover",overlayStyle:o=c,bgColor:m=p,viewBox:g="0 -1 24 24"}){const u=(0,n.DP)(),b={...t,color:t.color||u.colors.grayscale.base};return(0,a.Y)(s,{title:(0,a.Y)(d,{children:e}),placement:i,trigger:r,overlayStyle:o,color:m,children:(0,a.Y)(h,{children:(0,a.Y)(l.F.InfoCircleFilled,{"aria-label":"info-tooltip","data-test":"info-tooltip-icon",iconSize:"m",style:b,viewBox:g})})})}},40458:(e,t,i)=>{i.d(t,{A:()=>a});var n=i(96453),r=i(2445);const o=n.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
`,l=n.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
  &::after {
    display: inline-block;
    margin-left: ${({theme:e})=>e.gridUnit}px;
    color: ${({theme:e})=>e.colors.error.base};
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
    content: '*';
  }
`;function a({children:e,htmlFor:t,required:i=!1,className:n}){const a=i?l:o;return(0,r.Y)(a,{htmlFor:t,className:n,children:e})}},40563:(e,t,i)=>{i.d(t,{lV:()=>a,eI:()=>s.A,lR:()=>d.A,MA:()=>c.A});var n=i(77925),r=i(96453),o=i(2445);const l=(0,r.I4)(n.A)`
  &.ant-form label {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }
  .ant-form-item {
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }
`,a=Object.assign((function(e){return(0,o.Y)(l,{...e})}),{useForm:n.A.useForm,Item:n.A.Item,List:n.A.List,ErrorList:n.A.ErrorList,Provider:n.A.Provider});var s=i(86523),d=i(40458),c=i(97987)},45418:(e,t,i)=>{i.d(t,{A:()=>b});var n=i(96540),r=i(46942),o=i.n(r),l=i(22553),a=i(13147),s=i(6311),d=i(1051),c=i(96424),h=i(14277);const p=e=>{const{componentCls:t}=e;return{[t]:{"&-horizontal":{[`&${t}`]:{"&-sm":{marginBlock:e.marginXS},"&-md":{marginBlock:e.margin}}}}}},m=e=>{const{componentCls:t,sizePaddingEdgeHorizontal:i,colorSplit:n,lineWidth:r,textPaddingInline:o,orientationMargin:l,verticalMarginInline:a}=e;return{[t]:Object.assign(Object.assign({},(0,d.dF)(e)),{borderBlockStart:`${(0,s.unit)(r)} solid ${n}`,"&-vertical":{position:"relative",top:"-0.06em",display:"inline-block",height:"0.9em",marginInline:a,marginBlock:0,verticalAlign:"middle",borderTop:0,borderInlineStart:`${(0,s.unit)(r)} solid ${n}`},"&-horizontal":{display:"flex",clear:"both",width:"100%",minWidth:"100%",margin:`${(0,s.unit)(e.marginLG)} 0`},[`&-horizontal${t}-with-text`]:{display:"flex",alignItems:"center",margin:`${(0,s.unit)(e.dividerHorizontalWithTextGutterMargin)} 0`,color:e.colorTextHeading,fontWeight:500,fontSize:e.fontSizeLG,whiteSpace:"nowrap",textAlign:"center",borderBlockStart:`0 ${n}`,"&::before, &::after":{position:"relative",width:"50%",borderBlockStart:`${(0,s.unit)(r)} solid transparent`,borderBlockStartColor:"inherit",borderBlockEnd:0,transform:"translateY(50%)",content:"''"}},[`&-horizontal${t}-with-text-start`]:{"&::before":{width:`calc(${l} * 100%)`},"&::after":{width:`calc(100% - ${l} * 100%)`}},[`&-horizontal${t}-with-text-end`]:{"&::before":{width:`calc(100% - ${l} * 100%)`},"&::after":{width:`calc(${l} * 100%)`}},[`${t}-inner-text`]:{display:"inline-block",paddingBlock:0,paddingInline:o},"&-dashed":{background:"none",borderColor:n,borderStyle:"dashed",borderWidth:`${(0,s.unit)(r)} 0 0`},[`&-horizontal${t}-with-text${t}-dashed`]:{"&::before, &::after":{borderStyle:"dashed none none"}},[`&-vertical${t}-dashed`]:{borderInlineStartWidth:r,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},"&-dotted":{background:"none",borderColor:n,borderStyle:"dotted",borderWidth:`${(0,s.unit)(r)} 0 0`},[`&-horizontal${t}-with-text${t}-dotted`]:{"&::before, &::after":{borderStyle:"dotted none none"}},[`&-vertical${t}-dotted`]:{borderInlineStartWidth:r,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},[`&-plain${t}-with-text`]:{color:e.colorText,fontWeight:"normal",fontSize:e.fontSize},[`&-horizontal${t}-with-text-start${t}-no-default-orientation-margin-start`]:{"&::before":{width:0},"&::after":{width:"100%"},[`${t}-inner-text`]:{paddingInlineStart:i}},[`&-horizontal${t}-with-text-end${t}-no-default-orientation-margin-end`]:{"&::before":{width:"100%"},"&::after":{width:0},[`${t}-inner-text`]:{paddingInlineEnd:i}}})}},g=(0,c.OF)("Divider",(e=>{const t=(0,h.mergeToken)(e,{dividerHorizontalWithTextGutterMargin:e.margin,sizePaddingEdgeHorizontal:0});return[m(t),p(t)]}),(e=>({textPaddingInline:"1em",orientationMargin:.05,verticalMarginInline:e.marginXS})),{unitless:{orientationMargin:!0}});const u={small:"sm",middle:"md"},b=e=>{const{getPrefixCls:t,direction:i,className:r,style:s}=(0,l.TP)("divider"),{prefixCls:d,type:c="horizontal",orientation:h="center",orientationMargin:p,className:m,rootClassName:b,children:v,dashed:f,variant:$="solid",plain:x,style:w,size:y}=e,k=function(e,t){var i={};for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&t.indexOf(n)<0&&(i[n]=e[n]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var r=0;for(n=Object.getOwnPropertySymbols(e);r<n.length;r++)t.indexOf(n[r])<0&&Object.prototype.propertyIsEnumerable.call(e,n[r])&&(i[n[r]]=e[n[r]])}return i}(e,["prefixCls","type","orientation","orientationMargin","className","rootClassName","children","dashed","variant","plain","style","size"]),I=t("divider",d),[S,F,z]=g(I),A=(0,a.A)(y),Y=u[A],C=!!v,O=n.useMemo((()=>"left"===h?"rtl"===i?"end":"start":"right"===h?"rtl"===i?"start":"end":h),[i,h]),E="start"===O&&null!=p,H="end"===O&&null!=p,M=o()(I,r,F,z,`${I}-${c}`,{[`${I}-with-text`]:C,[`${I}-with-text-${O}`]:C,[`${I}-dashed`]:!!f,[`${I}-${$}`]:"solid"!==$,[`${I}-plain`]:!!x,[`${I}-rtl`]:"rtl"===i,[`${I}-no-default-orientation-margin-start`]:E,[`${I}-no-default-orientation-margin-end`]:H,[`${I}-${Y}`]:!!Y},m,b),B=n.useMemo((()=>"number"==typeof p?p:/^\d+$/.test(p)?Number(p):p),[p]),D={marginInlineStart:E?B:void 0,marginInlineEnd:H?B:void 0};return S(n.createElement("div",Object.assign({className:M,style:Object.assign(Object.assign({},s),w)},k,{role:"separator"}),v&&"vertical"!==c&&n.createElement("span",{className:`${I}-inner-text`,style:D},v)))}},50317:(e,t,i)=>{i.d(t,{A:()=>m});var n=i(96540),r=i(17437),o=i(96453),l=i(78518),a=i(66537),s=i(19129),d=i(40563),c=i(67073),h=i(2445);const p=r.AH`
  &.anticon {
    font-size: unset;
    .anticon {
      line-height: unset;
      vertical-align: unset;
    }
  }
`,m=({name:e,label:t,description:i,validationErrors:m=[],renderTrigger:g=!1,rightNode:u,leftNode:b,onClick:v,hovered:f=!1,tooltipOnClick:$=()=>{},warning:x,danger:w})=>{const{gridUnit:y,colors:k}=(0,o.DP)(),I=(0,n.useRef)(!1),S=(0,n.useMemo)((()=>(m.length||(I.current=!0),I.current?m.length?k.error.base:"unset":k.warning.base)),[k.error.base,k.warning.base,m.length]);return t?(0,h.FD)("div",{className:"ControlHeader","data-test":`${e}-header`,children:[(0,h.Y)("div",{className:"pull-left",children:(0,h.FD)(d.lR,{css:e=>r.AH`
            margin-bottom: ${.5*e.gridUnit}px;
            position: relative;
          `,children:[b&&(0,h.Y)("span",{children:b}),(0,h.Y)("span",{role:"button",tabIndex:0,onClick:v,style:{cursor:v?"pointer":""},children:t})," ",x&&(0,h.FD)("span",{children:[(0,h.Y)(s.m_,{id:"error-tooltip",placement:"top",title:x,children:(0,h.Y)(c.F.WarningOutlined,{iconColor:k.warning.base,css:r.AH`
                    vertical-align: baseline;
                  `,iconSize:"s"})})," "]}),w&&(0,h.FD)("span",{children:[(0,h.Y)(s.m_,{id:"error-tooltip",placement:"top",title:w,children:(0,h.Y)(c.F.ExclamationCircleOutlined,{iconColor:k.error.base,iconSize:"s"})})," "]}),(null==m?void 0:m.length)>0&&(0,h.FD)("span",{"data-test":"error-tooltip",children:[(0,h.Y)(s.m_,{id:"error-tooltip",placement:"top",title:null==m?void 0:m.join(" "),children:(0,h.Y)(c.F.ExclamationCircleOutlined,{css:r.AH`
                    ${p};
                    color: ${S};
                  `})})," "]}),f?(0,h.FD)("span",{css:()=>r.AH`
          position: absolute;
          top: 50%;
          right: 0;
          padding-left: ${y}px;
          transform: translate(100%, -50%);
          white-space: nowrap;
        `,children:[i&&(0,h.FD)("span",{children:[(0,h.Y)(s.m_,{id:"description-tooltip",title:i,placement:"top",children:(0,h.Y)(c.F.InfoCircleOutlined,{css:p,onClick:$})})," "]}),g&&(0,h.FD)("span",{children:[(0,h.Y)(a.W,{label:(0,l.t)("bolt"),tooltip:(0,l.t)("Changing this control takes effect instantly"),placement:"top",icon:"bolt"})," "]})]}):null]})}),u&&(0,h.Y)("div",{className:"pull-right",children:u}),(0,h.Y)("div",{className:"clearfix"})]}):null}},67874:(e,t,i)=>{i.d(t,{JF:()=>a,Mo:()=>s,YH:()=>o,j3:()=>l});var n=i(96453),r=i(86523);const o=0,l=n.I4.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e===o?"100%":`${e}px`};
`,a=(0,n.I4)(r.A)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,s=n.I4.div`
  color: ${({theme:e,status:t="error"})=>{var i;return null==(i=e.colors[t])?void 0:i.base}};
`},78697:(e,t,i)=>{i.d(t,{s:()=>l});var n=i(75160),r=i(26526),o=i(2445);const l=Object.assign(n.Ay,{GroupWrapper:({spaceConfig:e,options:t,...i})=>{const n=t.map((e=>(0,o.Y)(l,{value:e.value,children:e.label},e.value)));return(0,o.Y)(l.Group,{...i,children:e?(0,o.Y)(r.$,{...e,children:n}):n})},Button:n.Ay.Button})},87615:(e,t,i)=>{i.r(t),i.d(t,{default:()=>h});var n=i(96453),r=i(96627),o=i(96540),l=i(39074),a=i(67874),s=i(2445);const d=(0,n.I4)(a.j3)`
  display: flex;
  align-items: center;
  overflow-x: auto;

  & .ant-tag {
    margin-right: 0;
  }
`,c=n.I4.div`
  display: flex;
  height: 100%;
  max-width: 100%;
  width: 100%;
  & > div,
  & > div:hover {
    ${({validateStatus:e,theme:t})=>{var i;return e&&`border-color: ${null==(i=t.colors[e])?void 0:i.base}`}}
  }
`;function h(e){var t;const{setDataMask:i,setHoveredFilter:n,unsetHoveredFilter:a,setFocusedFilter:h,unsetFocusedFilter:p,setFilterActive:m,width:g,height:u,filterState:b,inputRef:v,isOverflowingFilterBar:f=!1}=e,$=(0,o.useCallback)((e=>{const t=e&&e!==r.WC;i({extraFormData:t?{time_range:e}:{},filterState:{value:t?e:void 0}})}),[i]);return(0,o.useEffect)((()=>{$(b.value)}),[b.value]),null!=(t=e.formData)&&t.inView?(0,s.Y)(d,{width:g,height:u,children:(0,s.Y)(c,{ref:v,validateStatus:b.validateStatus,onFocus:h,onBlur:p,onMouseEnter:n,onMouseLeave:a,children:(0,s.Y)(l.Ay,{value:b.value||r.WC,name:e.formData.nativeFilterId||"time_range",onChange:$,onOpenPopover:()=>m(!0),onClosePopover:()=>{m(!1),a(),p()},isOverflowingFilterBar:f})})}):null}},90868:(e,t,i)=>{i.d(t,{YI:()=>l,fs:()=>a,pd:()=>o});var n=i(11795),r=i(80566);const o=n.A,l=r.A,{TextArea:a}=n.A},97987:(e,t,i)=>{i.d(t,{A:()=>S});var n,r=i(96453),o=i(17437),l=i(78518),a=i(19129),s=i(90868),d=i(31641),c=i(67073),h=i(46920),p=i(96540);function m(){return m=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var i=arguments[t];for(var n in i)({}).hasOwnProperty.call(i,n)&&(e[n]=i[n])}return e},m.apply(null,arguments)}const g=({title:e,titleId:t,...i},r)=>p.createElement("svg",m({xmlns:"http://www.w3.org/2000/svg",width:24,height:24,fill:"none",ref:r,"aria-labelledby":t},i),e?p.createElement("title",{id:t},e):null,n||(n=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M12 7a1 1 0 0 0-1 1v4a1 1 0 1 0 2 0V8a1 1 0 0 0-1-1m0 8a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9.71-7.44-5.27-5.27a1.05 1.05 0 0 0-.71-.29H8.27a1.05 1.05 0 0 0-.71.29L2.29 7.56a1.05 1.05 0 0 0-.29.71v7.46c.004.265.107.518.29.71l5.27 5.27c.192.183.445.286.71.29h7.46a1.05 1.05 0 0 0 .71-.29l5.27-5.27a1.05 1.05 0 0 0 .29-.71V8.27a1.05 1.05 0 0 0-.29-.71M20 15.31 15.31 20H8.69L4 15.31V8.69L8.69 4h6.62L20 8.69z",clipRule:"evenodd"}))),u=(0,p.forwardRef)(g);var b=i(86523),v=i(40458),f=i(2445);const $=(0,r.I4)(s.pd)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,x=(0,r.I4)(s.pd.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,w=(0,r.I4)("div")`
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  .ant-form-item {
    margin-bottom: 0;
  }
`,y=r.I4.div`
  display: flex;
  align-items: center;
`,k=(0,r.I4)(v.A)`
  margin-bottom: 0;
`,I=o.AH`
  &.anticon > * {
    line-height: 0;
  }
`,S=({label:e,validationMethods:t,errorMessage:i,helpText:n,required:r=!1,hasTooltip:s=!1,tooltipText:p,id:m,className:g,visibilityToggle:v,get_url:S,description:F,...z})=>(0,f.FD)(w,{className:g,children:[(0,f.FD)(y,{children:[(0,f.Y)(k,{htmlFor:m,required:r,children:e}),s&&(0,f.Y)(d.A,{tooltip:`${p}`})]}),(0,f.FD)(b.A,{css:e=>((e,t)=>o.AH`
  .ant-form-item-children-icon {
    display: none;
  }
  ${t&&`.ant-form-item-control-input-content {\n      position: relative;\n      &:after {\n        content: ' ';\n        display: inline-block;\n        background: ${e.colors.error.base};\n        mask: url(${u});\n        mask-size: cover;\n        width: ${4*e.gridUnit}px;\n        height: ${4*e.gridUnit}px;\n        position: absolute;\n        right: ${1.25*e.gridUnit}px;\n        top: ${2.75*e.gridUnit}px;\n      }\n    }`}
`)(e,!!i),validateTrigger:Object.keys(t),validateStatus:i?"error":"success",help:i||n,hasFeedback:!!i,children:[v||"password"===z.name?(0,f.Y)(x,{...z,...t,iconRender:e=>e?(0,f.Y)(a.m_,{title:(0,l.t)("Hide password."),children:(0,f.Y)(c.F.EyeInvisibleOutlined,{iconSize:"m",css:I})}):(0,f.Y)(a.m_,{title:(0,l.t)("Show password."),children:(0,f.Y)(c.F.EyeOutlined,{iconSize:"m",css:I,"data-test":"icon-eye"})}),role:"textbox"}):(0,f.Y)($,{...z,...t}),S&&F?(0,f.FD)(h.A,{type:"link",htmlType:"button",buttonStyle:"default",onClick:()=>(window.open(S),!0),children:["Get ",F]}):(0,f.Y)("br",{})]})]})}}]);