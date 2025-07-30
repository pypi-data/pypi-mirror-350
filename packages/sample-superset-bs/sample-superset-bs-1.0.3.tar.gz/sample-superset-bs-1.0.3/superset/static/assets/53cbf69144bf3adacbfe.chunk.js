"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4229],{5007:(e,t,a)=>{function s(e){const t="CssEditor-css",a=document.head||document.getElementsByTagName("head")[0],s=document.querySelector(`.${t}`)||function(e){const t=document.createElement("style");return t.className=e,t.type="text/css",t}(t);return"styleSheet"in s?s.styleSheet.cssText=e:s.innerHTML=e,a.appendChild(s),function(){s.remove()}}a.d(t,{A:()=>s})},39093:(e,t,a)=>{a.d(t,{Au:()=>o,I8:()=>d,J:()=>l,l6:()=>i});var s=a(35742),n=a(5362);const r=(e,t,a)=>{let s=`/api/v1/dashboard/${e}/filter_state`;return t&&(s=s.concat(`/${t}`)),a&&(s=s.concat(`?tab_id=${a}`)),s},i=(e,t,a,i)=>s.A.put({endpoint:r(e,a,i),jsonPayload:{value:t}}).then((e=>e.json.message)).catch((e=>(n.A.error(e),null))),o=(e,t,a)=>s.A.post({endpoint:r(e,void 0,a),jsonPayload:{value:t}}).then((e=>e.json.key)).catch((e=>(n.A.error(e),null))),d=(e,t)=>s.A.get({endpoint:r(e,t)}).then((({json:e})=>JSON.parse(e.value))).catch((e=>(n.A.error(e),null))),l=e=>s.A.get({endpoint:`/api/v1/dashboard/permalink/${e}`}).then((({json:e})=>e)).catch((e=>(n.A.error(e),null)))},47986:(e,t,a)=>{a.d(t,{z:()=>r});var s=a(73992);function n(e,t){return e.length===Object.keys(t).length}function r(e,t,a){var r;let i=[];const o=Object.keys(a).includes(e)&&(0,s.Ub)(t),d=Array.isArray(t.scope)?t.scope:null!=(r=t.chartsInScope)?r:[];o&&(i=function(e,t,a){if(!t[e])return[];const s=[...a.filter((t=>String(t)!==e)),Number(e)],r=new Set(a);return Object.values(t).reduce(((a,i)=>i.slice_id===Number(e)?a:n(s,t)?(a.push(i.slice_id),a):(r.has(i.slice_id)&&a.push(i.slice_id),a)),[])}(e,a,d));const l=t;return(!o||(0,s.ve)(l)||(0,s.qQ)(l))&&(i=function(e,t){if(n(t,e))return Object.keys(e).map(Number);const a=new Set(t);return Object.values(e).reduce(((e,t)=>(a.has(t.slice_id)&&e.push(t.slice_id),e)),[])}(a,d)),i}},71478:(e,t,a)=>{a.d(t,{IX:()=>S.IX,hT:()=>s.hT,z7:()=>C.z7,PG:()=>C.PG,oh:()=>b,RG:()=>m,MZ:()=>y,DT:()=>w,RO:()=>E,IV:()=>x,Ip:()=>S.Ip,ii:()=>C.ii,rq:()=>C.rq,ty:()=>C.ty});var s=a(51066),n=a(86274),r=a(96540),i=a(86963),o=a(43031);const d=o.F.injectEndpoints({endpoints:e=>({catalogs:e.query({providesTags:[{type:"Catalogs",id:"LIST"}],query:({dbId:e,forceRefresh:t})=>({endpoint:`/api/v1/database/${e}/catalogs/`,urlParams:{force:t},transformResponse:({json:e})=>e.result.sort().map((e=>({value:e,label:e,title:e})))}),serializeQueryArgs:({queryArgs:{dbId:e}})=>({dbId:e})})})}),{useLazyCatalogsQuery:l,useCatalogsQuery:c,endpoints:u,util:h}=d,p=[];function b(e){const{dbId:t,onSuccess:a,onError:s}=e||{},[n]=l(),o=c({dbId:t,forceRefresh:!1},{skip:!t});(0,r.useEffect)((()=>{o.isError&&(null==s||s(o.error))}),[o.isError,o.error,s]);const d=(0,i.A)(((e,t=!1)=>{!e||o.currentData&&!t||n({dbId:e,forceRefresh:t}).then((({isSuccess:e,isError:n,data:r})=>{e&&(null==a||a(r||p,t)),n&&(null==s||s(o.error))}))})),u=(0,r.useCallback)((()=>{d(t,!0)}),[t,d]);return(0,r.useEffect)((()=>{d(t,!1)}),[t,d]),{...o,refetch:u}}var f=a(58561);function g({owners:e}){return e?e.map((e=>`${e.first_name} ${e.last_name}`)):null}const v=a.n(f)().encode({columns:["owners.first_name","owners.last_name"],keys:["none"]});function m(e){return(0,n.vL)((0,n.b5)(`/api/v1/chart/${e}?q=${v}`),g)}const y=e=>(0,n.vL)((0,n.b5)(`/api/v1/dashboard/${e}`),(e=>({...e,metadata:e.json_metadata&&JSON.parse(e.json_metadata)||{},position_data:e.position_json&&JSON.parse(e.position_json),owners:e.owners||[]}))),w=e=>(0,n.b5)(`/api/v1/dashboard/${e}/charts`),E=e=>(0,n.b5)(`/api/v1/dashboard/${e}/datasets`);var C=a(42242),S=a(3247);const I=o.F.injectEndpoints({endpoints:e=>({queryValidations:e.query({providesTags:["QueryValidations"],query:({dbId:e,catalog:t,schema:a,sql:s,templateParams:n})=>{let r=n;try{r=JSON.parse(n||"")}catch(e){r=void 0}const i={catalog:t,schema:a,sql:s,...r&&{template_params:r}};return{method:"post",endpoint:`/api/v1/database/${e}/validate_sql/`,headers:{"Content-Type":"application/json"},body:JSON.stringify(i),transformResponse:({json:e})=>e.result}}})})}),{useQueryValidationsQuery:x}=I},92008:(e,t,a)=>{a.d(t,{R:()=>n,W:()=>s});const s=(e,t)=>Object.values(e).filter((e=>e[t])).reduce(((e,a)=>({...e,[a.id]:t?a[t]:a})),{}),n=({chartConfiguration:e,nativeFilters:t,dataMask:a,allSliceIds:s})=>{const n={};return Object.values(a).forEach((({id:a,extraFormData:r={}})=>{var i,o,d,l,c,u,h,p,b;const f=null!=(i=null!=(o=null!=(d=null==t||null==(l=t[a])?void 0:l.chartsInScope)?d:null==e||null==(c=e[parseInt(a,10)])||null==(u=c.crossFilters)?void 0:u.chartsInScope)?o:s)?i:[],g=null==t||null==(h=t[a])?void 0:h.filterType,v=null!=(p=null==t||null==(b=t[a])?void 0:b.targets)?p:f;n[a]={scope:f,filterType:g,targets:v,values:r}})),n}},94229:(e,t,a)=>{a.r(t),a.d(t,{DashboardPage:()=>ue,DashboardPageIdContext:()=>ie,default:()=>he});var s=a(96540),n=a(17437),r=a(61574),i=a(96453),o=a(78518),d=a(61225),l=a(1081),c=a(5261),u=a(17444),h=a(71478),p=a(52123),b=a(34975),f=a(5007),g=a(92008),v=a(68921),m=a(62221),y=a(27023),w=a(32132),E=a(72173),C=a(39093),S=a(82960),I=a(5556),x=a.n(I),_=a(36053),D=a(38708),$=a(49588);function j(e){return Object.values(e).reduce(((e,t)=>(t&&t.type===$.oT&&t.meta&&t.meta.chartId&&e.push(t.meta.chartId),e)),[])}var O=a(4881),T=a(35700),k=a(35839),F=a(37725);const R=[$.oT,$.xY,$.rG];function U(e){return!Object.values(e).some((({type:e})=>e&&R.includes(e)))}var M=a(47986),q=a(2445);const A={actions:x().shape({addSliceToDashboard:x().func.isRequired,removeSliceFromDashboard:x().func.isRequired,triggerQuery:x().func.isRequired,logEvent:x().func.isRequired,clearDataMaskState:x().func.isRequired}).isRequired,dashboardId:x().number.isRequired,editMode:x().bool,isPublished:x().bool,hasUnsavedChanges:x().bool,slices:x().objectOf(O.VE).isRequired,activeFilters:x().object.isRequired,chartConfiguration:x().object,datasources:x().object.isRequired,ownDataCharts:x().object.isRequired,layout:x().object.isRequired,impressionId:x().string.isRequired,timeout:x().number,userId:x().string,children:x().node};class P extends s.PureComponent{static onBeforeUnload(e){e?window.addEventListener("beforeunload",P.unload):window.removeEventListener("beforeunload",P.unload)}static unload(){const e=(0,o.t)("You have unsaved changes.");return window.event.returnValue=e,e}constructor(e){var t,a;super(e),this.appliedFilters=null!=(t=e.activeFilters)?t:{},this.appliedOwnDataCharts=null!=(a=e.ownDataCharts)?a:{},this.onVisibilityChange=this.onVisibilityChange.bind(this)}componentDidMount(){const e=(0,D.Ay)(),{editMode:t,isPublished:a,layout:s}=this.props,n={is_soft_navigation:T.Vy.timeOriginOffset>0,is_edit_mode:t,mount_duration:T.Vy.getTimestamp(),is_empty:U(s),is_published:a,bootstrap_data_length:e.length},r=(0,F.A)();r&&(n.target_id=r),this.props.actions.logEvent(T.es,n),"hidden"===document.visibilityState&&(this.visibilityEventData={start_offset:T.Vy.getTimestamp(),ts:(new Date).getTime()}),window.addEventListener("visibilitychange",this.onVisibilityChange),this.applyCharts()}componentDidUpdate(){this.applyCharts()}UNSAFE_componentWillReceiveProps(e){const t=j(this.props.layout),a=j(e.layout);this.props.dashboardId===e.dashboardId&&(t.length<a.length?a.filter((e=>-1===t.indexOf(e))).forEach((t=>{return this.props.actions.addSliceToDashboard(t,(a=e.layout,s=t,Object.values(a).find((e=>e&&e.type===$.oT&&e.meta&&e.meta.chartId===s))));var a,s})):t.length>a.length&&t.filter((e=>-1===a.indexOf(e))).forEach((e=>this.props.actions.removeSliceFromDashboard(e))))}applyCharts(){const{activeFilters:e,ownDataCharts:t,chartConfiguration:a,hasUnsavedChanges:s,editMode:n}=this.props,{appliedFilters:r,appliedOwnDataCharts:i}=this;a&&(n||(0,k.r$)(i,t,{ignoreUndefined:!0})&&(0,k.r$)(r,e,{ignoreUndefined:!0})||this.applyFilters(),s?P.onBeforeUnload(!0):P.onBeforeUnload(!1))}componentWillUnmount(){window.removeEventListener("visibilitychange",this.onVisibilityChange),this.props.actions.clearDataMaskState()}onVisibilityChange(){if("hidden"===document.visibilityState)this.visibilityEventData={start_offset:T.Vy.getTimestamp(),ts:(new Date).getTime()};else if("visible"===document.visibilityState){const e=this.visibilityEventData.start_offset;this.props.actions.logEvent(T.Xj,{...this.visibilityEventData,duration:T.Vy.getTimestamp()-e})}}applyFilters(){const{appliedFilters:e}=this,{activeFilters:t,ownDataCharts:a,slices:s}=this.props,n=Object.keys(t),r=Object.keys(e),i=new Set(n.concat(r)),o=((e,t)=>{const a=Object.keys(e),s=Object.keys(t),n=(r=a,i=s,[...r.filter((e=>!i.includes(e))),...i.filter((e=>!r.includes(e)))]).filter((a=>e[a]||t[a]));var r,i;return new Set([...a,...s]).forEach((a=>{(0,k.r$)(e[a],t[a])||n.push(a)})),[...new Set(n)]})(a,this.appliedOwnDataCharts);[...i].forEach((a=>{if(!n.includes(a)&&r.includes(a))o.push(...(0,M.z)(a,e[a],s));else if(r.includes(a)){if((0,k.r$)(e[a].values,t[a].values,{ignoreUndefined:!0})||o.push(...(0,M.z)(a,t[a],s)),!(0,k.r$)(e[a].scope,t[a].scope)){const s=(t[a].scope||[]).concat(e[a].scope||[]);o.push(...s)}}else o.push(...(0,M.z)(a,t[a],s))})),this.refreshCharts([...new Set(o)]),this.appliedFilters=t,this.appliedOwnDataCharts=a}refreshCharts(e){e.forEach((e=>{this.props.actions.triggerQuery(!0,e)}))}render(){return this.context.loading?(0,q.Y)(u.A,{}):this.props.children}}P.contextType=_.bf,P.propTypes=A,P.defaultProps={timeout:60,userId:""};const z=P;var V=a(2514),L=a(7735),N=a(95004);const H=(0,d.Ng)((function(e){var t,a,s;const{datasources:n,sliceEntities:r,dashboardInfo:i,dashboardState:o,dashboardLayout:d,impressionId:l}=e;return{timeout:null==(t=i.common)||null==(a=t.conf)?void 0:a.SUPERSET_WEBSERVER_TIMEOUT,userId:i.userId,dashboardId:i.id,editMode:o.editMode,isPublished:o.isPublished,hasUnsavedChanges:o.hasUnsavedChanges,datasources:n,chartConfiguration:null==(s=i.metadata)?void 0:s.chart_configuration,slices:r.slices,layout:d.present,impressionId:l}}),(function(e){return{actions:(0,S.zH)({setDatasources:b.nC,clearDataMaskState:N.V9,addSliceToDashboard:E.ft,removeSliceFromDashboard:E.Hg,triggerQuery:V.triggerQuery,logEvent:L.logEvent},e)}}))(z);var Q=a(43561);const Y=e=>n.AH`
  body {
    h1 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xxl}px;
      letter-spacing: -0.2px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${3*e.gridUnit}px;
    }

    h2 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xl}px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    h3,
    h4,
    h5,
    h6 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.l}px;
      letter-spacing: 0.2px;
      margin-top: ${2*e.gridUnit}px;
      margin-bottom: ${e.gridUnit}px;
    }
  }
`,B=e=>n.AH`
  .header-title a {
    margin: ${e.gridUnit/2}px;
    padding: ${e.gridUnit/2}px;
  }
  .header-controls {
    &,
    &:hover {
      margin-top: ${e.gridUnit}px;
    }
  }
`,J=e=>n.AH`
  .antd5-dropdown-menu.chart-context-menu {
    min-width: ${43*e.gridUnit}px;
  }
  .antd5-dropdown-menu-submenu.chart-context-submenu {
    max-width: ${60*e.gridUnit}px;
    min-width: ${40*e.gridUnit}px;
  }
`,W=e=>n.AH`
  a,
  .ant-tabs-tabpane,
  .ant-tabs-tab-btn,
  .superset-button,
  .superset-button.antd5-dropdown-trigger,
  .header-controls span {
    &:focus-visible {
      box-shadow: 0 0 0 2px ${e.colors.primary.dark1};
      border-radius: ${e.gridUnit/2}px;
      outline: none;
      text-decoration: none;
    }
    &:not(
        .superset-button,
        .antd5-menu-item,
        a,
        .fave-unfave-icon,
        .ant-tabs-tabpane,
        .header-controls span
      ) {
      &:focus-visible {
        padding: ${e.gridUnit/2}px;
      }
    }
  }
`;var X=a(71086),G=a.n(X),K=a(44383),Z=a.n(K),ee=a(55556);const te={},ae=()=>{const e=(0,m.Gq)(m.Hh.DashboardExploreContext,{});return G()(e,(e=>!e.isRedundant))},se=(e,t)=>{const a=ae();(0,m.SO)(m.Hh.DashboardExploreContext,{...a,[e]:{...t,dashboardPageId:e}})},ne=(0,l.Mz)([e=>e.dashboardInfo.metadata,e=>e.dashboardInfo.id,e=>{var t;return null==(t=e.dashboardState)?void 0:t.colorScheme},e=>{var t;return null==(t=e.nativeFilters)?void 0:t.filters},e=>e.dataMask],((e,t,a,s,n)=>{const r=Object.keys(s).reduce(((e,t)=>(e[t]=Z()(s[t],["chartsInScope"]),e)),{});return{labelsColor:(null==e?void 0:e.label_colors)||te,labelsColorMap:(null==e?void 0:e.map_label_colors)||te,sharedLabelsColors:(0,ee.ik)(null==e?void 0:e.shared_label_colors),colorScheme:a,chartConfiguration:(null==e?void 0:e.chart_configuration)||te,nativeFilters:r,dataMask:n,dashboardId:t,filterBoxFilters:(0,v.ug)()}})),re=({dashboardPageId:e})=>{const t=(0,d.d4)(ne);return(0,s.useEffect)((()=>(se(e,t),()=>{se(e,{...t,isRedundant:!0})})),[t,e]),null},ie=(0,s.createContext)(""),oe=(0,s.lazy)((()=>Promise.all([a.e(2885),a.e(8948),a.e(7232),a.e(1343),a.e(9924),a.e(8700),a.e(4e3),a.e(9666),a.e(5160),a.e(8963),a.e(6845),a.e(4922),a.e(5386),a.e(3321),a.e(1723),a.e(9285),a.e(217),a.e(9968),a.e(554),a.e(9074),a.e(6738),a.e(8604),a.e(833),a.e(3463),a.e(5026)]).then(a.bind(a,20630)))),de=document.title,le=(0,l.Mz)((e=>e.dataMask),(e=>(0,g.W)(e,"ownState"))),ce=(0,l.Mz)([e=>{var t;return null==(t=e.dashboardInfo.metadata)?void 0:t.chart_configuration},e=>e.nativeFilters.filters,e=>e.dataMask,e=>e.dashboardState.sliceIds],((e,t,a,s)=>({...(0,v.ug)(),...(0,g.R)({chartConfiguration:e,nativeFilters:t,dataMask:a,allSliceIds:s})}))),ue=({idOrSlug:e})=>{const t=(0,i.DP)(),a=(0,d.wA)(),l=(0,r.W6)(),g=(0,s.useMemo)((()=>(0,Q.Ak)()),[]),v=(0,d.d4)((({dashboardInfo:e})=>e&&Object.keys(e).length>0)),{addDangerToast:S}=(0,c.Yf)(),{result:I,error:x}=(0,h.MZ)(e),{result:_,error:D}=(0,h.DT)(e),{result:$,error:j,status:O}=(0,h.RO)(e),T=(0,s.useRef)(!1),k=x||D,F=Boolean(I&&_),{dashboard_title:R,css:U,id:M=0}=I||{};(0,s.useEffect)((()=>{const e=()=>{const e=ae();(0,m.SO)(m.Hh.DashboardExploreContext,{...e,[g]:{...e[g],isRedundant:!0}})};return window.addEventListener("beforeunload",e),()=>{window.removeEventListener("beforeunload",e)}}),[g]),(0,s.useEffect)((()=>{a((0,E.wh)(O))}),[a,O]),(0,s.useEffect)((()=>{M&&async function(){const e=(0,w.P3)(y.vX.permalinkKey),t=(0,w.P3)(y.vX.nativeFiltersKey),s=(0,w.P3)(y.vX.nativeFilters);let n,r=t||{};if(e){const t=await(0,C.J)(e);t&&({dataMask:r,activeTabs:n}=t.state)}else t&&(r=await(0,C.I8)(M,t));s&&(r=s),F&&(T.current||(T.current=!0),a((0,p.M)({history:l,dashboard:I,charts:_,activeTabs:n,dataMask:r})))}()}),[F]),(0,s.useEffect)((()=>(R&&(document.title=R),()=>{document.title=de})),[R]),(0,s.useEffect)((()=>"string"==typeof U?(0,f.A)(U):()=>{}),[U]),(0,s.useEffect)((()=>{j?S((0,o.t)("Error loading chart datasources. Filters may not work correctly.")):a((0,b.nC)($))}),[S,$,j,a]);const A=(0,d.d4)(le),P=(0,d.d4)(ce);if(k)throw k;const z=(0,s.useMemo)((()=>[n.AH`
  .filter-card-tooltip {
    &.antd5-tooltip-placement-bottom {
      padding-top: 0;
      & .antd5-tooltip-arrow {
        top: -13px;
      }
    }
  }
`,Y(t),J(t),W(t),B(t)]),[t]);if(k)throw k;const V=(0,s.useMemo)((()=>(0,q.Y)(oe,{})),[]);return(0,q.FD)(q.FK,{children:[(0,q.Y)(n.mL,{styles:z}),F&&v?(0,q.FD)(q.FK,{children:[(0,q.Y)(re,{dashboardPageId:g}),(0,q.Y)(ie.Provider,{value:g,children:(0,q.Y)(H,{activeFilters:P,ownDataCharts:A,children:V})})]}):(0,q.Y)(u.A,{})]})},he=ue}}]);