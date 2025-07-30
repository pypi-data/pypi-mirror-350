"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9074],{6094:(e,t,n)=>{n.d(t,{c:()=>o,l:()=>r});var a=n(8729),i=n(17437),l=n(2445);const r=e=>(0,l.Y)(a.A,{css:i.AH`
      width: 100%;
    `,...e}),o=a.A.RangePicker},7987:(e,t,n)=>{n.d(t,{RV:()=>s,be:()=>r,cJ:()=>c,ke:()=>d,kw:()=>u,o6:()=>l,oF:()=>i,sw:()=>a,u_:()=>o});const a="previous calendar week",i="previous calendar month",l="previous calendar quarter",r="previous calendar year",o="Current day",d="Current week",c="Current month",s="Current year",u="Current quarter"},13686:(e,t,n)=>{n.d(t,{t:()=>m});var a=n(77189);const i=String.raw`\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:(?:[+-]\d\d:\d\d)|Z)?`,l=String.raw`(?:TODAY|NOW)`,r=String.raw`[+-]?[1-9][0-9]*`,o=String.raw`YEAR|QUARTER|MONTH|WEEK|DAY|HOUR|MINUTE|SECOND`,d=RegExp(String.raw`^DATEADD\(DATETIME\("(${i}|${l})"\),\s(${r}),\s(${o})\)$`,"i"),c=RegExp(String.raw`^${i}$|^${l}$`,"i"),s=["now","today"],u=new Date;u.setHours(0,0,0,0);const h=new Date;h.setHours(0,0,0,0);const p={sinceDatetime:u.setDate(u.getDate()-7).toString(),sinceMode:"relative",sinceGrain:"day",sinceGrainValue:-7,untilDatetime:h.toString(),untilMode:"specific",untilGrain:"day",untilGrainValue:7,anchorMode:"now",anchorValue:"now"},m=e=>{const t=e.split(a.wv);if(2===t.length){const[e,n]=t;if(c.test(e)&&c.test(n)){const t=s.includes(e)?e:"specific",a=s.includes(n)?n:"specific";return{customRange:{...p,sinceDatetime:e,untilDatetime:n,sinceMode:t,untilMode:a},matchedFlag:!0}}const a=e.match(d);if(a&&c.test(n)&&e.includes(n)){const[e,t,i]=a.slice(1),l=s.includes(n)?n:"specific";return{customRange:{...p,sinceGrain:i,sinceGrainValue:parseInt(t,10),sinceDatetime:e,untilDatetime:e,sinceMode:"relative",untilMode:l},matchedFlag:!0}}const i=n.match(d);if(c.test(e)&&i&&n.includes(e)){const[t,n,a]=[...i.slice(1)],l=s.includes(e)?e:"specific";return{customRange:{...p,untilGrain:a,untilGrainValue:parseInt(n,10),sinceDatetime:t,untilDatetime:t,untilMode:"relative",sinceMode:l},matchedFlag:!0}}if(a&&i){const[e,t,n]=[...a.slice(1)],[l,r,o]=[...i.slice(1)];if(e===l)return{customRange:{...p,sinceGrain:n,sinceGrainValue:parseInt(t,10),sinceDatetime:e,untilGrain:o,untilGrainValue:parseInt(r,10),untilDatetime:l,anchorValue:e,sinceMode:"relative",untilMode:"relative",anchorMode:"now"===e?"now":"specific"},matchedFlag:!0}}}return{customRange:p,matchedFlag:!1}}},22533:(e,t,n)=>{n.d(t,{A:()=>d,v:()=>r});var a=n(96540),i=n(64535),l=n(2445);const r=()=>{var e;return null==(e=document.getElementById("controlSections"))?void 0:e.lastElementChild},o=e=>{var t,n;const a=null==(t=window)?void 0:t.innerHeight,i=null==(n=window)?void 0:n.innerWidth,l=null==e?void 0:e.getBoundingClientRect();return a&&i&&null!=l&&l.top?{yRatio:l.top/a,xRatio:l.left/i}:{yRatio:0,xRatio:0}},d=({getPopupContainer:e,getVisibilityRatio:t=o,open:n,destroyTooltipOnHide:d=!1,placement:c="right",...s})=>{const u=(0,a.useRef)(),[h,p]=(0,a.useState)(void 0===n?s.defaultOpen:n),[m,v]=a.useState(c),g=(0,a.useCallback)((()=>{if(!u.current)return;const{yRatio:e,xRatio:n}=t(u.current),a=n<.35?"right":n>.65?"left":"",i=e<.35?a?"top":"bottom":e>.65?a?"bottom":"top":"",l=(a?a+i.charAt(0).toUpperCase()+i.slice(1):i)||"left";l!==m&&v(l)}),[t]),f=(0,a.useCallback)((e=>{const t=r();t&&t.style.setProperty("overflow-y",e?"hidden":"auto","important")}),[g]),b=(0,a.useCallback)((t=>(u.current=t,(null==e?void 0:e(t))||document.body)),[g,e]),y=(0,a.useCallback)((e=>{void 0===e&&f(e),p(!!e),null==s.onOpenChange||s.onOpenChange(!!e)}),[s,f]),C=(0,a.useCallback)((e=>{"Escape"===e.key&&(p(!1),null==s.onOpenChange||s.onOpenChange(!1))}),[s]);return(0,a.useEffect)((()=>{void 0!==n&&p(!!n)}),[n]),(0,a.useEffect)((()=>{void 0!==h&&f(h)}),[h,f]),(0,a.useEffect)((()=>(h&&document.addEventListener("keydown",C),()=>{document.removeEventListener("keydown",C)})),[C,h]),(0,a.useEffect)((()=>{h&&g()}),[h,g]),(0,l.Y)(i.A,{...s,open:h,arrow:{pointAtCenter:!0},placement:m,onOpenChange:y,getPopupContainer:b,destroyTooltipOnHide:d})}},28532:(e,t,n)=>{n.d(t,{Y:()=>d});var a=n(74353),i=n.n(a),l=n(96540),r=n(61225);n(65826),n(813),n(47317),n(33900),n(16033),n(50952),n(50494),n(72369),n(92218),n(62796),n(88003),n(46847),n(39998),n(69423);const o={en:()=>n.e(5543).then(n.bind(n,75543)),fr:()=>n.e(6930).then(n.bind(n,26930)),es:()=>n.e(254).then(n.bind(n,70254)),it:()=>n.e(2432).then(n.bind(n,32432)),zh:()=>n.e(2441).then(n.bind(n,32441)),ja:()=>n.e(2963).then(n.bind(n,72963)),de:()=>n.e(5700).then(n.bind(n,5700)),pt:()=>n.e(126).then(n.bind(n,40126)),pt_BR:()=>n.e(3898).then(n.bind(n,3898)),ru:()=>n.e(12).then(n.bind(n,10012)),ko:()=>n.e(9605).then(n.bind(n,39605)),sk:()=>n.e(3266).then(n.bind(n,3266)),sl:()=>n.e(1271).then(n.bind(n,41271)),nl:()=>n.e(9414).then(n.bind(n,9414))},d=()=>{const[e,t]=(0,l.useState)(null),n=(0,r.d4)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.locale}));return(0,l.useEffect)((()=>{null===e&&(n&&o[n]?o[n]().then((e=>{t(e.default),i().locale(n)})).catch((()=>t(void 0))):t(void 0))}),[e,n]),e}},39074:(e,t,n)=>{n.d(t,{Ay:()=>a.A});var a=n(45267);n(39942)},39942:(e,t,n)=>{n.d(t,{cn:()=>c,oo:()=>y,nS:()=>s,z6:()=>o,Be:()=>b,OL:()=>d,yI:()=>C,ZC:()=>u,Ex:()=>h,c1:()=>Y,ad:()=>D,BJ:()=>r,bd:()=>w,IZ:()=>m,Wm:()=>g,s6:()=>v,OP:()=>f,IS:()=>S,Ab:()=>x,J5:()=>R,IM:()=>k});var a=n(7089),i=n(78518),l=n(7987);const r=[{value:"Common",label:(0,i.t)("Last")},{value:"Calendar",label:(0,i.t)("Previous")},{value:"Current",label:(0,i.t)("Current")},{value:"Custom",label:(0,i.t)("Custom")},{value:"Advanced",label:(0,i.t)("Advanced")},{value:"No filter",label:(0,i.t)("No filter")}],o=[{value:"Last day",label:(0,i.t)("Last day")},{value:"Last week",label:(0,i.t)("Last week")},{value:"Last month",label:(0,i.t)("Last month")},{value:"Last quarter",label:(0,i.t)("Last quarter")},{value:"Last year",label:(0,i.t)("Last year")}],d=new Set(o.map((e=>e.value))),c=[{value:l.sw,label:(0,i.t)("previous calendar week")},{value:l.oF,label:(0,i.t)("previous calendar month")},{value:l.o6,label:(0,i.t)("previous calendar quarter")},{value:l.be,label:(0,i.t)("previous calendar year")}],s=new Set(c.map((e=>e.value))),u=[{value:l.u_,label:(0,i.t)("Current day")},{value:l.ke,label:(0,i.t)("Current week")},{value:l.cJ,label:(0,i.t)("Current month")},{value:l.kw,label:(0,i.t)("Current quarter")},{value:l.RV,label:(0,i.t)("Current year")}],h=new Set(u.map((e=>e.value))),p=[{value:"second",label:e=>(0,i.t)("Seconds %s",e)},{value:"minute",label:e=>(0,i.t)("Minutes %s",e)},{value:"hour",label:e=>(0,i.t)("Hours %s",e)},{value:"day",label:e=>(0,i.t)("Days %s",e)},{value:"week",label:e=>(0,i.t)("Weeks %s",e)},{value:"month",label:e=>(0,i.t)("Months %s",e)},{value:"quarter",label:e=>(0,i.t)("Quarters %s",e)},{value:"year",label:e=>(0,i.t)("Years %s",e)}],m=p.map((e=>({value:e.value,label:e.label((0,i.t)("Before"))}))),v=p.map((e=>({value:e.value,label:e.label((0,i.t)("After"))}))),g=[{value:"specific",label:(0,i.t)("Specific Date/Time")},{value:"relative",label:(0,i.t)("Relative Date/Time")},{value:"now",label:(0,i.t)("Now")},{value:"today",label:(0,i.t)("Midnight")}],f=g.slice(),b=new Set(["Last day","Last week","Last month","Last quarter","Last year"]),y=new Set([l.sw,l.oF,l.o6,l.be]),C=new Set([l.u_,l.ke,l.cJ,l.kw,l.RV]),Y="YYYY-MM-DD[T]HH:mm:ss",w=((0,a.XV)().utc().startOf("day").subtract(7,"days").format(Y),(0,a.XV)().utc().startOf("day").format(Y));var D;!function(e){e.CommonFrame="common-frame",e.ModalOverlay="modal-overlay",e.PopoverOverlay="time-range-trigger",e.NoFilter="no-filter",e.CancelButton="cancel-button",e.ApplyButton="date-filter-control__apply-button"}(D||(D={}));const A=String.raw`\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:(?:[+-]\d\d:\d\d)|Z)?`,$=String.raw`(?:TODAY|NOW)`,E=(RegExp(String.raw`^${A}$|^${$}$`,"i"),["specific","today","now"]),x=e=>"now"===e?(0,a.XV)().utc().startOf("second"):"today"===e?(0,a.XV)().utc().startOf("day"):(0,a.XV)(e),F=e=>x(e).format(Y),S=e=>{const{sinceDatetime:t,sinceMode:n,sinceGrain:a,sinceGrainValue:i,untilDatetime:l,untilMode:r,untilGrain:o,untilGrainValue:d,anchorValue:c}={...e};if(E.includes(n)&&E.includes(r))return`${"specific"===n?F(t):n} : ${"specific"===r?F(l):r}`;if(E.includes(n)&&"relative"===r){const e="specific"===n?F(t):n;return`${e} : DATEADD(DATETIME("${e}"), ${d}, ${o})`}if("relative"===n&&E.includes(r)){const e="specific"===r?F(l):r;return`DATEADD(DATETIME("${e}"), ${-Math.abs(i)}, ${a}) : ${e}`}return`DATEADD(DATETIME("${c}"), ${-Math.abs(i)}, ${a}) : DATEADD(DATETIME("${c}"), ${d}, ${o})`};var T=n(96627),N=n(13686),I=n(61225);const R=e=>d.has(e)?"Common":s.has(e)?"Calendar":h.has(e)?"Current":e===T.WC?"No filter":(0,N.t)(e).matchedFlag?"Custom":"Advanced";function k(){var e;return null!=(e=(0,I.d4)((e=>{var t,n;return null==e||null==(t=e.common)||null==(n=t.conf)?void 0:n.DEFAULT_TIME_FILTER})))?e:T.WC}},45267:(e,t,n)=>{n.d(t,{A:()=>Z});var a=n(96540),i=n(96453),l=n(17437),r=n(37827),o=n(96627),d=n(77189),c=n(78518),s=n(46920),u=n(50317),h=n(85861),p=n(85955),m=n(67073),v=n(28990),g=n(19129),f=n(85183),b=n(27023),y=n(15151),C=n(22533),Y=n(39942),w=n(78697),D=n(2445);function A(e){let t="Last week";return Y.Be.has(e.value)?t=e.value:e.onChange(t),(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title","data-test":Y.ad.CommonFrame,children:(0,c.t)("Configure Time Range: Last...")}),(0,D.Y)(w.s.GroupWrapper,{spaceConfig:{direction:"vertical",size:15,align:"start",wrap:!1},size:"large",value:t,onChange:t=>e.onChange(t.target.value),options:Y.z6})]})}var $=n(7987);function E({onChange:e,value:t}){return(0,a.useEffect)((()=>{Y.oo.has(t)||e($.sw)}),[e,t]),Y.oo.has(t)?(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Previous...")}),(0,D.Y)(w.s.GroupWrapper,{spaceConfig:{direction:"vertical",size:15,align:"start",wrap:!1},size:"large",value:t,onChange:t=>e(t.target.value),options:Y.cn})]}):null}function x({onChange:e,value:t}){return(0,a.useEffect)((()=>{Y.yI.has(t)||e($.ke)}),[t]),Y.yI.has(t)?(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Current...")}),(0,D.Y)(w.s.GroupWrapper,{spaceConfig:{direction:"vertical",size:15,align:"start",wrap:!0},size:"large",onChange:t=>{let n=t.target.value;n=n.trim(),""!==n&&e(n)},options:Y.ZC})]}):null}var F=n(13686),S=n(66537),T=n(15595),N=n(90868),I=n(6094),R=n(17444),k=n(23807),M=n(28532);function V(e){const{customRange:t,matchedFlag:n}=(0,F.t)(e.value),a=(0,M.Y)();n||e.onChange((0,Y.IS)(t));const{sinceDatetime:i,sinceMode:l,sinceGrain:r,sinceGrainValue:o,untilDatetime:d,untilMode:s,untilGrain:u,untilGrainValue:h,anchorValue:p,anchorMode:m}={...t};function g(n,a){e.onChange((0,Y.IS)({...t,[n]:a}))}function f(n,a){"number"==typeof a&&Number.isInteger(a)&&a>0&&e.onChange((0,Y.IS)({...t,[n]:a}))}return null===a?(0,D.Y)(R.A,{position:"inline-centered"}):(0,D.Y)(k.Q,{locale:a,children:(0,D.FD)("div",{"data-test":"custom-frame",children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure custom time range")}),(0,D.FD)(T.fI,{gutter:24,children:[(0,D.FD)(T.fv,{span:12,children:[(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("START (INCLUSIVE)")," ",(0,D.Y)(S.W,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})]}),(0,D.Y)(v.A,{ariaLabel:(0,c.t)("START (INCLUSIVE)"),options:Y.Wm,value:l,onChange:e=>g("sinceMode",e)}),"specific"===l&&(0,D.Y)(T.fI,{children:(0,D.Y)(I.l,{showTime:!0,defaultValue:(0,Y.Ab)(i),onChange:e=>g("sinceDatetime",e.format(Y.c1)),allowClear:!1,getPopupContainer:t=>e.isOverflowingFilterBar?t.parentNode:document.body})}),"relative"===l&&(0,D.FD)(T.fI,{gutter:8,children:[(0,D.Y)(T.fv,{span:11,children:(0,D.Y)(N.YI,{placeholder:(0,c.t)("Relative quantity"),value:Math.abs(o),min:1,defaultValue:1,onChange:e=>f("sinceGrainValue",e||1),onStep:e=>f("sinceGrainValue",e||1)})}),(0,D.Y)(T.fv,{span:13,children:(0,D.Y)(v.A,{ariaLabel:(0,c.t)("Relative period"),options:Y.IZ,value:r,onChange:e=>g("sinceGrain",e)})})]})]}),(0,D.FD)(T.fv,{span:12,children:[(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("END (EXCLUSIVE)")," ",(0,D.Y)(S.W,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})]}),(0,D.Y)(v.A,{ariaLabel:(0,c.t)("END (EXCLUSIVE)"),options:Y.OP,value:s,onChange:e=>g("untilMode",e)}),"specific"===s&&(0,D.Y)(T.fI,{children:(0,D.Y)(I.l,{showTime:!0,defaultValue:(0,Y.Ab)(d),onChange:e=>g("untilDatetime",e.format(Y.c1)),allowClear:!1,getPopupContainer:t=>e.isOverflowingFilterBar?t.parentNode:document.body})}),"relative"===s&&(0,D.FD)(T.fI,{gutter:8,children:[(0,D.Y)(T.fv,{span:11,children:(0,D.Y)(N.YI,{placeholder:(0,c.t)("Relative quantity"),value:h,min:1,defaultValue:1,onChange:e=>f("untilGrainValue",e||1),onStep:e=>f("untilGrainValue",e||1)})}),(0,D.Y)(T.fv,{span:13,children:(0,D.Y)(v.A,{ariaLabel:(0,c.t)("Relative period"),options:Y.s6,value:u,onChange:e=>g("untilGrain",e)})})]})]})]}),"relative"===l&&"relative"===s&&(0,D.FD)("div",{className:"control-anchor-to",children:[(0,D.Y)("div",{className:"control-label",children:(0,c.t)("Anchor to")}),(0,D.FD)(T.fI,{align:"middle",children:[(0,D.Y)(T.fv,{children:(0,D.Y)(w.s.GroupWrapper,{options:[{value:"now",label:(0,c.t)("Now")},{value:"specific",label:(0,c.t)("Date/Time")}],onChange:function(n){const a=n.target.value;"now"===a?e.onChange((0,Y.IS)({...t,anchorValue:"now",anchorMode:a})):e.onChange((0,Y.IS)({...t,anchorValue:Y.bd,anchorMode:a}))},defaultValue:"now",value:m})}),"now"!==m&&(0,D.Y)(T.fv,{children:(0,D.Y)(I.l,{showTime:!0,defaultValue:(0,Y.Ab)(p),onChange:e=>g("anchorValue",e.format(Y.c1)),allowClear:!1,className:"control-anchor-to-datetime",getPopupContainer:t=>e.isOverflowingFilterBar?t.parentNode:document.body})})]})]})]})})}const O=(0,D.FD)(D.FK,{children:[(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATETIME"}),(0,D.Y)("p",{children:(0,c.t)("Return to specific datetime.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"datetime([string])"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'datetime("2020-03-01 12:00:00")\ndatetime("now")\ndatetime("last year")'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATEADD"}),(0,D.Y)("p",{children:(0,c.t)("Moves the given set of dates by a specified interval.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"dateadd([datetime], [integer], [dateunit])\ndateunit = (year | quarter | month | week | day | hour | minute | second)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'dateadd(datetime("today"), -13, day)\ndateadd(datetime("2020-03-01"), 2, day)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATETRUNC"}),(0,D.Y)("p",{children:(0,c.t)("Truncates the specified date to the accuracy specified by the date unit.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"datetrunc([datetime], [dateunit])\ndateunit = (year | quarter | month | week)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'datetrunc(datetime("2020-03-01"), week)\ndatetrunc(datetime("2020-03-01"), month)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"LASTDAY"}),(0,D.Y)("p",{children:(0,c.t)("Get the last date by the date unit.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"lastday([datetime], [dateunit])\ndateunit = (year | month | week)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'lastday(datetime("today"), month)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"HOLIDAY"}),(0,D.Y)("p",{children:(0,c.t)("Get the specify date for the holiday")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"holiday([string])\nholiday([holiday string], [datetime])\nholiday([holiday string], [datetime], [country name])"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'holiday("new year")\nholiday("christmas", datetime("2019"))\nholiday("christmas", dateadd(datetime("2019"), 1, year))\nholiday("christmas", datetime("2 years ago"))\nholiday("Easter Monday", datetime("2019"), "UK")'})})]})]}),L=e=>{const t=(0,i.DP)();return(0,D.Y)(l.Z2,{children:({css:n})=>(0,D.Y)(g.m_,{overlayClassName:n`
            .antd5-tooltip-content {
              min-width: ${125*t.gridUnit}px;
              max-height: 410px;
              overflow-y: scroll;

              .antd5-tooltip-inner {
                max-width: ${125*t.gridUnit}px;
                h3 {
                  font-size: ${t.typography.sizes.m}px;
                  font-weight: ${t.typography.weights.bold};
                }
                h4 {
                  font-size: ${t.typography.sizes.m}px;
                  font-weight: ${t.typography.weights.bold};
                }
                pre {
                  border: none;
                  text-align: left;
                  word-break: break-word;
                  font-size: ${t.typography.sizes.s}px;
                }
              }
            }
          `,...e})})};function G(e){return(0,D.Y)(L,{title:O,...e})}function W(e){return e.includes(d.wv)?e:e.startsWith("Last")?[e,""].join(d.wv):e.startsWith("Next")?["",e].join(d.wv):d.wv}function P(e){const t=W(e.value||""),[n,a]=t.split(d.wv);function i(t,i){"since"===t?e.onChange(`${i}${d.wv}${a}`):e.onChange(`${n}${d.wv}${i}`)}return t!==e.value&&e.onChange(W(e.value||"")),(0,D.FD)(D.FK,{children:[(0,D.FD)("div",{className:"section-title",children:[(0,c.t)("Configure Advanced Time Range "),(0,D.Y)(G,{placement:"rightBottom",children:(0,D.Y)("i",{className:"fa fa-info-circle text-muted"})})]}),(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("START (INCLUSIVE)")," ",(0,D.Y)(S.W,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})]}),(0,D.Y)(N.pd,{value:n,onChange:e=>i("since",e.target.value)},"since"),(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("END (EXCLUSIVE)")," ",(0,D.Y)(S.W,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})]}),(0,D.Y)(N.pd,{value:a,onChange:e=>i("until",e.target.value)},"until")]})}const z="#45BED6",U=i.I4.div`
  ${({theme:e,isActive:t,isPlaceholder:n})=>l.AH`
    width: 100%;
    height: ${8*e.gridUnit}px;

    display: flex;
    align-items: center;
    flex-wrap: nowrap;

    padding: 0 ${3*e.gridUnit}px;

    background-color: ${e.colors.grayscale.light5};

    border: 1px solid
      ${t?z:e.colors.grayscale.light2};
    border-radius: ${e.borderRadius}px;

    cursor: pointer;

    transition: border-color 0.3s cubic-bezier(0.65, 0.05, 0.36, 1);
    :hover,
    :focus {
      border-color: ${z};
    }

    .date-label-content {
      color: ${n?e.colors.grayscale.light1:e.colors.grayscale.dark1};
      overflow: hidden;
      text-overflow: ellipsis;
      min-width: 0;
      flex-shrink: 1;
      white-space: nowrap;
    }

    span[role='img'] {
      margin-left: auto;
      padding-left: ${e.gridUnit}px;

      & > span[role='img'] {
        line-height: 0;
      }
    }
  `}
`,B=(0,a.forwardRef)(((e,t)=>(0,D.FD)(U,{...e,tabIndex:0,role:"button",children:[(0,D.Y)("span",{id:`date-label-${e.name}`,className:"date-label-content",ref:t,children:"string"==typeof e.label?(0,c.t)(e.label):e.label}),(0,D.Y)(m.F.CalendarOutlined,{iconSize:"s"})]}))),H=(0,i.I4)(v.A)`
  width: 272px;
`,_=i.I4.div`
  ${({theme:e})=>l.AH`
    .ant-row {
      margin-top: 8px;
    }

    .antd5-input-number {
      width: 100%;
    }

    .ant-picker {
      padding: 4px 17px 4px;
      border-radius: 4px;
      width: 100%;
    }

    .antd5-divider-horizontal {
      margin: 16px 0;
    }

    .control-label {
      font-size: 11px;
      font-weight: ${e.typography.weights.medium};
      color: ${e.colors.grayscale.light2};
      line-height: 16px;
      margin: 8px 0;
    }

    .section-title {
      font-style: normal;
      font-weight: ${e.typography.weights.bold};
      font-size: 15px;
      line-height: 24px;
      margin-bottom: 8px;
    }

    .control-anchor-to {
      margin-top: 16px;
    }

    .control-anchor-to-datetime {
      width: 217px;
    }

    .footer {
      text-align: right;
    }
  `}
`,q=i.I4.span`
  span {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
    vertical-align: middle;
  }
  .text {
    vertical-align: middle;
  }
  .error {
    color: ${({theme:e})=>e.colors.error.base};
  }
`,K=(e,t,n)=>e?(0,D.FD)("div",{children:[t&&(0,D.Y)("strong",{children:t}),n&&(0,D.Y)("div",{css:e=>l.AH`
            margin-top: ${e.gridUnit}px;
          `,children:n})]}):n||null;function Z(e){var t;const{name:n,onChange:l,onOpenPopover:v=y.fZ,onClosePopover:w=y.fZ,overlayStyle:$="Popover",isOverflowingFilterBar:F=!1}=e,S=(0,Y.IM)(),T=null!=(t=e.value)?t:S,[N,I]=(0,a.useState)(T),[R,k]=(0,a.useState)(!1),M=(0,a.useMemo)((()=>(0,Y.J5)(T)),[T]),[O,L]=(0,a.useState)(M),[G,W]=(0,a.useState)(T),[z,U]=(0,a.useState)(T),[Z,X]=(0,a.useState)(!1),[j,J]=(0,a.useState)(T),[Q,ee]=(0,a.useState)(T),te=(0,i.DP)(),[ne,ae]=(0,r.A)();function ie(){U(T),L(M),k(!1),w()}(0,a.useEffect)((()=>{if(T===o.WC)return I(o.WC),ee(null),void X(!0);(0,d.x9)(T).then((({value:e,error:t})=>{if(t)J(t||""),X(!1),ee(T||null);else{if("Common"===M||"Calendar"===M||"Current"===M||"No filter"===M)I(T),ee(K(ae,T,e));else{let t=e||"";"Custom"===M&&(t=function(e){const t=e.match(/(\d{4}-\d{2}-\d{2})(?:T\d{2}:\d{2}:\d{2})?\s*([^]*?)\s*(\d{4}-\d{2}-\d{2})(?:T\d{2}:\d{2}:\d{2})?/);return t?`${t[1]} ${t[2].trim()} ${t[3]}`:null}(e)||t),I(e||""),ee(K(ae,t,T))}X(!0)}W(T),J(e||T)}))}),[M,ae,ne,T]),(0,f.sv)((()=>{if(z===o.WC)return J(o.WC),W(o.WC),void X(!0);G!==z&&(0,d.x9)(z).then((({value:e,error:t})=>{t?(J(t||""),X(!1)):(J(e||""),X(!0)),W(z)}))}),b.Qs,[z]);const le=()=>{R?ie():(U(T),L(M),k(!0),v())},re=(0,D.FD)(_,{children:[(0,D.Y)("div",{className:"control-label",children:(0,c.t)("RANGE TYPE")}),(0,D.Y)(H,{ariaLabel:(0,c.t)("RANGE TYPE"),options:Y.BJ,value:O,onChange:function(e){e===o.WC&&U(o.WC),L(e)}}),"No filter"!==O&&(0,D.Y)(p.c,{}),"Common"===O&&(0,D.Y)(A,{value:z,onChange:U}),"Calendar"===O&&(0,D.Y)(E,{value:z,onChange:U}),"Current"===O&&(0,D.Y)(x,{value:z,onChange:U}),"Advanced"===O&&(0,D.Y)(P,{value:z,onChange:U}),"Custom"===O&&(0,D.Y)(V,{value:z,onChange:U,isOverflowingFilterBar:F}),"No filter"===O&&(0,D.Y)("div",{"data-test":Y.ad.NoFilter}),(0,D.Y)(p.c,{}),(0,D.FD)("div",{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Actual time range")}),Z&&(0,D.Y)("div",{children:"No filter"===j?(0,c.t)("No filter"):j}),!Z&&(0,D.FD)(q,{className:"warning",children:[(0,D.Y)(m.F.ExclamationCircleOutlined,{iconColor:te.colors.error.base}),(0,D.Y)("span",{className:"text error",children:j})]})]}),(0,D.Y)(p.c,{}),(0,D.FD)("div",{className:"footer",children:[(0,D.Y)(s.A,{buttonStyle:"secondary",cta:!0,onClick:ie,"data-test":Y.ad.CancelButton,children:(0,c.t)("CANCEL")},"cancel"),(0,D.Y)(s.A,{buttonStyle:"primary",cta:!0,disabled:!Z,onClick:function(){l(z),k(!1),w()},"data-test":Y.ad.ApplyButton,children:(0,c.t)("APPLY")},"apply")]})]}),oe=(0,D.FD)(q,{children:[(0,D.Y)(m.F.EditOutlined,{}),(0,D.Y)("span",{className:"text",children:(0,c.t)("Edit time range")})]}),de=(0,D.Y)(C.A,{autoAdjustOverflow:!1,trigger:"click",placement:"right",content:re,title:oe,defaultOpen:R,open:R,onOpenChange:le,overlayStyle:{width:"600px"},destroyTooltipOnHide:!0,getPopupContainer:e=>F?e.parentNode:document.body,overlayClassName:"time-range-popover",children:(0,D.Y)(g.m_,{placement:"top",title:Q,children:(0,D.Y)(B,{name:n,"aria-labelledby":`filter-name-${e.name}`,"aria-describedby":`date-label-${e.name}`,label:N,isActive:R,isPlaceholder:N===o.WC,"data-test":Y.ad.PopoverOverlay,ref:ne})})}),ce=(0,D.FD)(D.FK,{children:[(0,D.Y)(g.m_,{placement:"top",title:Q,children:(0,D.Y)(B,{name:n,"aria-labelledby":`filter-name-${e.name}`,"aria-describedby":`date-label-${e.name}`,onClick:le,label:N,isActive:R,isPlaceholder:N===o.WC,"data-test":Y.ad.ModalOverlay,ref:ne})}),(0,D.Y)(h.Ay,{title:oe,show:R,onHide:le,width:"600px",hideFooter:!0,zIndex:1030,children:re})]});return(0,D.FD)(D.FK,{children:[(0,D.Y)(u.A,{...e}),"Modal"===$?ce:de]})}},64535:(e,t,n)=>{n.d(t,{A:()=>l});var a=n(66265),i=n(2445);const l=e=>(0,i.Y)(a.A,{...e})},77189:(e,t,n)=>{n.d(t,{wv:()=>s,x9:()=>m});var a=n(62193),i=n.n(a),l=n(58561),r=n.n(l),o=n(62952),d=n(35742),c=n(51436);const s=" : ",u=(e,t)=>`${e}${s}${t}`,h=(e,t)=>e.replace("T00:00:00","")||(t?"-∞":"∞"),p=(e,t="col")=>{const n=e.split(s);return 1===n.length?e:`${h(n[0],!0)} ≤ ${t} < ${h(n[1])}`},m=async(e,t="col",n)=>{let a,l;if(i()(n))a=r().encode_uri(e),l=`/api/v1/time_range/?q=${a}`;else{const t=(0,o.A)(n).map((t=>({timeRange:e,shift:t})));a=r().encode_uri([{timeRange:e},...t]),l=`/api/v1/time_range/?q=${a}`}try{var m;const e=await d.A.get({endpoint:l});if(i()(n)){var v,g,f,b;const n=u((null==e||null==(v=e.json)||null==(g=v.result[0])?void 0:g.since)||"",(null==e||null==(f=e.json)||null==(b=f.result[0])?void 0:b.until)||"");return{value:p(n,t)}}const a=null==e||null==(m=e.json)?void 0:m.result.map((e=>u(e.since,e.until)));return{value:a.slice(1).map((e=>((e,t,n="col")=>{const a=e.split(s),i=t.split(s);return`${n}: ${h(a[0],!0)} to ${h(a[1])} vs\n  ${h(i[0],!0)} to ${h(i[1])}`})(a[0],e,t)))}}catch(e){const t=await(0,c.h4)(e);return{error:t.message||t.error||e.statusText}}}},85955:(e,t,n)=>{n.d(t,{c:()=>l});var a=n(45418),i=n(2445);function l(e){return(0,i.Y)(a.A,{...e})}}}]);