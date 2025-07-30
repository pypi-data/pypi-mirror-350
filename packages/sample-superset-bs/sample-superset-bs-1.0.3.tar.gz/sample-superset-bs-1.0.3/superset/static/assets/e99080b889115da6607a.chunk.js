"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3849],{6094:(e,t,n)=>{n.d(t,{c:()=>o,l:()=>r});var a=n(8729),l=n(17437),i=n(2445);const r=e=>(0,i.Y)(a.A,{css:l.AH`
      width: 100%;
    `,...e}),o=a.A.RangePicker},28532:(e,t,n)=>{n.d(t,{Y:()=>s});var a=n(74353),l=n.n(a),i=n(96540),r=n(61225);n(65826),n(813),n(47317),n(33900),n(16033),n(50952),n(50494),n(72369),n(92218),n(62796),n(88003),n(46847),n(39998),n(69423);const o={en:()=>n.e(5543).then(n.bind(n,75543)),fr:()=>n.e(6930).then(n.bind(n,26930)),es:()=>n.e(254).then(n.bind(n,70254)),it:()=>n.e(2432).then(n.bind(n,32432)),zh:()=>n.e(2441).then(n.bind(n,32441)),ja:()=>n.e(2963).then(n.bind(n,72963)),de:()=>n.e(5700).then(n.bind(n,5700)),pt:()=>n.e(126).then(n.bind(n,40126)),pt_BR:()=>n.e(3898).then(n.bind(n,3898)),ru:()=>n.e(12).then(n.bind(n,10012)),ko:()=>n.e(9605).then(n.bind(n,39605)),sk:()=>n.e(3266).then(n.bind(n,3266)),sl:()=>n.e(1271).then(n.bind(n,41271)),nl:()=>n.e(9414).then(n.bind(n,9414))},s=()=>{const[e,t]=(0,i.useState)(null),n=(0,r.d4)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.locale}));return(0,i.useEffect)((()=>{null===e&&(n&&o[n]?o[n]().then((e=>{t(e.default),l().locale(n)})).catch((()=>t(void 0))):t(void 0))}),[e,n]),e}},43849:(e,t,n)=>{n.d(t,{t:()=>ye,A:()=>ve});var a=n(96453),l=n(78518),i=n(96540),r=n(25946),o=n(46942),s=n.n(o),d=n(46920),c=n(67073),u=n(85994),p=n(47251),g=n(73204),h=n(35742),m=n(40563),b=n(85861),f=n(49756),v=n(3932),y=n(2445);const x=a.I4.div`
  .bulk-tag-text {
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }
`,w=({show:e,selected:t=[],onHide:n,refreshData:a,resourceName:r,addSuccessToast:o,addDangerToast:s})=>{(0,i.useEffect)((()=>{}),[]);const[c,u]=(0,i.useState)([]);return(0,y.Y)(b.Ay,{title:(0,l.t)("Bulk tag"),show:e,onHide:()=>{u([]),n()},footer:(0,y.FD)("div",{children:[(0,y.Y)(d.A,{"data-test":"modal-save-dashboard-button",buttonStyle:"secondary",onClick:n,children:(0,l.t)("Cancel")}),(0,y.Y)(d.A,{"data-test":"modal-save-dashboard-button",buttonStyle:"primary",onClick:async()=>{await h.A.post({endpoint:"/api/v1/tag/bulk_create",jsonPayload:{tags:c.map((e=>({name:e.label,objects_to_tag:t.map((e=>[r,+e.original.id]))})))}}).then((({json:e={}})=>{const t=e.result.objects_skipped,n=e.result.objects_tagged;t.length>0&&o((0,l.t)("%s items could not be tagged because you don’t have edit permissions to all selected objects.",t.length,r)),o((0,l.t)("Tagged %s %ss",n.length,r))})).catch((e=>{s((0,l.t)("Failed to tag items"))})),a(),n(),u([])},children:(0,l.t)("Save")})]}),children:(0,y.FD)(x,{children:[(0,y.Y)("div",{className:"bulk-tag-text",children:(0,l.t)("You are adding tags to %s %ss",t.length,r)}),(0,y.Y)(m.lR,{children:(0,l.t)("tags")}),(0,y.Y)(f.A,{ariaLabel:"tags",value:c,options:v.m,onHide:n,onChange:e=>u(e),placeholder:(0,l.t)("Select Tags"),mode:"multiple"})]})})},S=a.I4.div`
  ${({theme:e,showThumbnails:t})=>`\n    display: grid;\n    grid-gap: ${12*e.gridUnit}px ${4*e.gridUnit}px;\n    grid-template-columns: repeat(auto-fit, 300px);\n    margin-top: ${-6*e.gridUnit}px;\n    padding: ${t?`${8*e.gridUnit+3}px ${9*e.gridUnit}px`:`${8*e.gridUnit+1}px ${9*e.gridUnit}px`};\n  `}
`,C=a.I4.div`
  border: 2px solid transparent;
  &.card-selected {
    border: 2px solid ${({theme:e})=>e.colors.primary.base};
  }
  &.bulk-select {
    cursor: pointer;
  }
`;function Y({bulkSelectEnabled:e,loading:t,prepareRow:n,renderCard:a,rows:l,showThumbnails:i}){return a?(0,y.FD)(S,{showThumbnails:i,children:[t&&0===l.length&&[...new Array(25)].map(((e,n)=>(0,y.Y)("div",{children:a({loading:t})},n))),l.length>0&&l.map((l=>a?(n(l),(0,y.Y)(C,{className:s()({"card-selected":e&&l.isSelected,"bulk-select":e}),onClick:t=>{return n=t,a=l.toggleRowSelected,void(e&&(n.preventDefault(),n.stopPropagation(),a()));var n,a},role:"none",children:a({...l.original,loading:t})},l.id)):null))]}):null}var k=n(98837),$=n(17437),I=n(90868),F=n(2404),T=n.n(F),_=n(32885),A=n(33231),D=n(58561),N=n.n(D);const P={encode:e=>void 0===e?void 0:N().encode(e).replace(/%/g,"%25").replace(/&/g,"%26").replace(/\+/g,"%2B").replace(/#/g,"%23"),decode:e=>void 0===e||Array.isArray(e)?void 0:N().decode(e)};class R extends Error{constructor(...e){super(...e),this.name="ListViewError"}}function B(e,t){return e.map((({id:e,urlDisplay:n,operator:a})=>({id:e,urlDisplay:n,operator:a,value:t[n||e]})))}function U(e,t){const n=[],a={};return Object.keys(e).forEach((t=>{const l={id:t,value:e[t]};a[t]=l,n.push(l)})),t.forEach((e=>{const t=e.urlDisplay||e.id,n=a[t];n&&(n.operator=e.operator,n.id=e.id)})),n}var E=n(31641);const z=a.I4.div`
  width: ${200}px;
`,V=(0,a.I4)(I.pd)`
  border-radius: ${({theme:e})=>e.gridUnit}px;
`;function H({Header:e,name:t,initialValue:n,toolTipDescription:r,onSubmit:o},s){const d=(0,a.DP)(),[u,p]=(0,i.useState)(n||""),g=()=>{u&&o(u.trim())};return(0,i.useImperativeHandle)(s,(()=>({clearFilter:()=>{p(""),o("")}}))),(0,y.FD)(z,{children:[(0,y.FD)("div",{css:$.AH`
          display: flex;
          align-items: start;
        `,children:[(0,y.Y)(m.lR,{children:e}),r&&(0,y.Y)(E.A,{tooltip:r,viewBox:"0 -7 28 28"})]}),(0,y.Y)(V,{allowClear:!0,"data-test":"filters-search",placeholder:(0,l.t)("Type a value"),name:t,value:u,onChange:e=>{p(e.currentTarget.value),""===e.currentTarget.value&&o("")},onPressEnter:g,onBlur:g,prefix:(0,y.Y)(c.F.SearchOutlined,{iconColor:d.colors.grayscale.light1,iconSize:"l"})})]})}const M=(0,i.forwardRef)(H);var O=n(15595);const L=a.I4.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
  width: ${200}px;
`;function j({Header:e,name:t,fetchSelects:n,initialValue:a,onSelect:r,selects:o=[],loading:s=!1},d){const[c,u]=(0,i.useState)(a),p=e=>{r(e?{label:e.label,value:e.value}:void 0),u(e)},g=()=>{r(void 0,!0),u(void 0)};(0,i.useImperativeHandle)(d,(()=>({clearFilter:()=>{g()}})));const h=(0,i.useMemo)((()=>async(e,t,a)=>{if(n){const l=await n(e,t,a);return{data:l.data,totalCount:l.totalCount}}return{data:[],totalCount:0}}),[n]);return(0,y.Y)(L,{children:n?(0,y.Y)(f.A,{allowClear:!0,ariaLabel:"string"==typeof e?e:t||(0,l.t)("Filter"),"data-test":"filters-select",header:(0,y.Y)(m.lR,{children:e}),onChange:p,onClear:g,options:h,placeholder:(0,l.t)("Select or type a value"),showSearch:!0,value:c}):(0,y.Y)(O.l6,{allowClear:!0,ariaLabel:"string"==typeof e?e:t||(0,l.t)("Filter"),"data-test":"filters-select",header:(0,y.Y)(m.lR,{children:e}),labelInValue:!0,onChange:p,onClear:g,options:o,placeholder:(0,l.t)("Select or type a value"),showSearch:!0,value:c,loading:s})})}const G=(0,i.forwardRef)(j);var q=n(6094),W=n(7089),K=n(17444),Q=n(23807),X=n(28532);const J=a.I4.div`
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  width: 360px;
`;function Z({Header:e,initialValue:t,onSubmit:n,dateFilterValueType:a="unix"},r){const[o,s]=(0,i.useState)(null!=t?t:null),d=(0,i.useMemo)((()=>!o||Array.isArray(o)&&!o.length?null:[(0,W.XV)(o[0]),(0,W.XV)(o[1])]),[o]),c=(0,X.Y)();return(0,i.useImperativeHandle)(r,(()=>({clearFilter:()=>{s(null),n([])}}))),null===c?(0,y.Y)(K.A,{position:"inline-centered"}):(0,y.Y)(Q.Q,{locale:c,children:(0,y.FD)(J,{children:[(0,y.Y)(m.lR,{children:e}),(0,y.Y)(q.c,{placeholder:[(0,l.t)("Start date"),(0,l.t)("End date")],showTime:!0,value:d,onCalendarChange:e=>{var t,l,i,r,o,d;if(null==e||null==(t=e[0])||!t.valueOf()||null==e||null==(l=e[1])||!l.valueOf())return s(null),void n([]);const c="iso"===a?[e[0].toISOString(),e[1].toISOString()]:[null!=(i=null==(r=e[0])?void 0:r.valueOf())?i:0,null!=(o=null==(d=e[1])?void 0:d.valueOf())?o:0];s(c),n(c)}})]})})}const ee=(0,i.forwardRef)(Z),te=a.I4.div`
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  width: 360px;
`,ne=a.I4.div`
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
`,ae=a.I4.span`
  margin: 0 ${({theme:e})=>2*e.gridUnit}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,le=a.I4.div`
  color: ${({theme:e})=>e.colors.error.base};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  position: absolute;
  bottom: -50%;
  left: 0;
`;function ie({Header:e,initialValue:t,onSubmit:n},a){const[r,o]=(0,i.useState)(null!=t?t:[null,null]),[s,d]=(0,i.useState)(!1);return(0,i.useImperativeHandle)(a,(()=>({clearFilter:()=>{o([null,null]),d(!1),n([null,null])}}))),(0,y.FD)(te,{children:[(0,y.Y)(m.lR,{children:e}),(0,y.FD)(ne,{children:[(0,y.Y)(I.YI,{value:r[0],onChange:e=>{const t=[e,r[1]];o(t),null!==e&&null!==r[1]&&e>=r[1]?d(!0):(d(!1),n(t))},placeholder:(0,l.t)("Value greater than"),style:{width:"100%"},"data-test":"numerical-filter-min-input"}),(0,y.Y)(ae,{children:"-"}),(0,y.Y)(I.YI,{value:r[1],onChange:e=>{const t=[r[0],e];o(t),null!==r[0]&&null!==e&&r[0]>=e?d(!0):(d(!1),n(t))},placeholder:(0,l.t)("Value less than"),style:{width:"100%"},"data-test":"numerical-filter-max-input"}),s&&(0,y.Y)(le,{children:(0,l.t)("Minimum must be strictly less than maximum")})]})]})}const re=(0,i.forwardRef)(ie);function oe({filters:e,internalFilters:t=[],updateFilterValue:n},a){const l=(0,i.useMemo)((()=>Array.from({length:e.length},(()=>(0,i.createRef)()))),[e.length]);return(0,i.useImperativeHandle)(a,(()=>({clearFilters:()=>{l.forEach((e=>{var t;null==(t=e.current)||null==t.clearFilter||t.clearFilter()}))}}))),(0,y.Y)(y.FK,{children:e.map((({Header:e,fetchSelects:a,key:i,id:r,input:o,paginate:s,selects:d,toolTipDescription:c,onFilterUpdate:u,loading:p,dateFilterValueType:g,min:h,max:m},b)=>{var f;const v=null==t||null==(f=t[b])?void 0:f.value;return"select"===o?(0,y.Y)(G,{ref:l[b],Header:e,fetchSelects:a,initialValue:v,name:r,onSelect:(e,t)=>{u&&(t||u(e)),n(b,e)},paginate:s,selects:d,loading:null!=p&&p},i):"search"===o&&"string"==typeof e?(0,y.Y)(M,{ref:l[b],Header:e,initialValue:v,name:r,toolTipDescription:c,onSubmit:e=>{u&&u(e),n(b,e)}},i):"datetime_range"===o?(0,y.Y)(ee,{ref:l[b],Header:e,initialValue:v,name:r,onSubmit:e=>n(b,e),dateFilterValueType:g||"unix"},i):"numerical_range"===o?(0,y.Y)(re,{ref:l[b],Header:e,initialValue:v,min:h,max:m,name:r,onSubmit:e=>n(b,e)},i):null}))})}const se=(0,k.b)((0,i.forwardRef)(oe)),de=a.I4.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
  text-align: left;
  width: ${200}px;
`,ce=({initialSort:e,onChange:t,options:n})=>{const a=e&&n.find((({id:t,desc:n})=>t===e[0].id&&n===e[0].desc))||n[0],[r,o]=(0,i.useState)({label:a.label,value:a.value}),s=(0,i.useMemo)((()=>n.map((e=>({label:e.label,value:e.value})))),[n]);return(0,y.Y)(de,{children:(0,y.Y)(O.l6,{ariaLabel:(0,l.t)("Sort"),header:(0,y.Y)(m.lR,{children:(0,l.t)("Sort")}),labelInValue:!0,onChange:e=>{o(e);const a=n.find((({value:t})=>t===e.value));if(a){const e=[{id:a.id,desc:a.desc}];t(e)}},options:s,showSearch:!0,value:r,"data-test":"card-sort-select"})})};var ue=n(50455);const pe=a.I4.div`
  text-align: center;

  .superset-list-view {
    text-align: left;
    border-radius: 4px 0;
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;

    .header {
      display: flex;
      padding-bottom: ${({theme:e})=>4*e.gridUnit}px;

      & .controls {
        display: flex;
        flex-wrap: wrap;
        column-gap: ${({theme:e})=>6*e.gridUnit}px;
        row-gap: ${({theme:e})=>4*e.gridUnit}px;
      }
    }

    .body.empty table {
      margin-bottom: 0;
    }

    .body {
      overflow-x: auto;
    }

    .antd5-empty {
      .antd5-empty-image {
        height: auto;
      }
    }
  }

  .pagination-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }

  .row-count-container {
    margin-top: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,ge=(0,a.I4)(r.A)`
  ${({theme:e})=>`\n    border-radius: 0;\n    margin-bottom: 0;\n    color: ${e.colors.grayscale.dark1};\n    background-color: ${e.colors.primary.light4};\n\n    .selectedCopy {\n      display: inline-block;\n      padding: ${2*e.gridUnit}px 0;\n    }\n\n    .deselect-all, .tag-btn {\n      color: ${e.colors.primary.base};\n      margin-left: ${4*e.gridUnit}px;\n    }\n\n    .divider {\n      margin: ${2*-e.gridUnit}px 0 ${2*-e.gridUnit}px ${4*e.gridUnit}px;\n      width: 1px;\n      height: ${8*e.gridUnit}px;\n      box-shadow: inset -1px 0px 0px ${e.colors.grayscale.light2};\n      display: inline-flex;\n      vertical-align: middle;\n      position: relative;\n    }\n\n    .ant-alert-close-icon {\n      margin-top: ${1.5*e.gridUnit}px;\n    }\n  `}
`,he={Cell:({row:e})=>(0,y.Y)(u.A,{...e.getToggleRowSelectedProps(),id:e.id}),Header:({getToggleAllRowsSelectedProps:e})=>(0,y.Y)(u.A,{...e(),id:"header-toggle-all","data-test":"header-toggle-all"}),id:"selection",size:"sm"},me=a.I4.div`
  padding-right: ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>5*e.gridUnit+1}px;
  white-space: nowrap;
  display: inline-block;

  .toggle-button {
    display: inline-block;
    border-radius: ${({theme:e})=>e.gridUnit/2}px;
    padding: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>.5*e.gridUnit}px;

    &:first-of-type {
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }
  }

  .active {
    background-color: ${({theme:e})=>e.colors.grayscale.base};
    svg {
      color: ${({theme:e})=>e.colors.grayscale.light5};
    }
  }
`,be=a.I4.div`
  padding: ${({theme:e})=>40*e.gridUnit}px 0;

  &.table {
    background: ${({theme:e})=>e.colors.grayscale.light5};
  }
`,fe=({mode:e,setMode:t})=>(0,y.FD)(me,{children:[(0,y.Y)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("card")},className:s()("toggle-button",{active:"card"===e}),children:(0,y.Y)(c.F.AppstoreOutlined,{iconSize:"xl"})}),(0,y.Y)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("table")},className:s()("toggle-button",{active:"table"===e}),children:(0,y.Y)(c.F.UnorderedListOutlined,{iconSize:"xl"})})]}),ve=function({columns:e,data:t,count:n,pageSize:a,fetchData:r,refreshData:o,loading:s,initialSort:c=[],className:u="",filters:h=[],bulkActions:m=[],bulkSelectEnabled:b=!1,disableBulkSelect:f=()=>{},renderBulkSelectCopy:v=e=>(0,l.t)("%s Selected",e.length),renderCard:x,showThumbnails:S,cardSortSelectOptions:C,defaultViewMode:k="card",highlightRowId:$,emptyState:I,columnsForWrapText:F,enableBulkTag:D=!1,bulkTagResourceName:N,addSuccessToast:E,addDangerToast:z}){const{getTableProps:V,getTableBodyProps:H,headerGroups:M,rows:O,prepareRow:L,pageCount:j=1,gotoPage:G,applyFilterValue:q,setSortBy:W,selectedFlatRows:K,toggleAllRowsSelected:Q,setViewMode:X,state:{pageIndex:J,pageSize:Z,internalFilters:ee,sortBy:te,viewMode:ne},query:ae}=function({fetchData:e,columns:t,data:n,count:a,initialPageSize:l,initialFilters:r=[],initialSort:o=[],bulkSelectMode:s=!1,bulkSelectColumnConfig:d,renderCard:c=!1,defaultViewMode:u="card"}){const[p,g]=(0,A.sq)({filters:P,pageIndex:A.hc,sortColumn:A.fr,sortOrder:A.fr,viewMode:A.fr}),h=(0,i.useMemo)((()=>p.sortColumn&&p.sortOrder?[{id:p.sortColumn,desc:"desc"===p.sortOrder}]:o),[o,p.sortColumn,p.sortOrder]),m={filters:p.filters?U(p.filters,r):[],pageIndex:p.pageIndex||0,pageSize:l,sortBy:h},[b,f]=(0,i.useState)(p.viewMode||(c?u:"table")),v=(0,i.useMemo)((()=>{const e=t.map((e=>({...e,filter:"exact"})));return s?[d,...e]:e}),[s,t]),{getTableProps:y,getTableBodyProps:x,headerGroups:w,rows:S,prepareRow:C,canPreviousPage:Y,canNextPage:k,pageCount:$,gotoPage:I,setAllFilters:F,setSortBy:D,selectedFlatRows:N,toggleAllRowsSelected:R,state:{pageIndex:E,pageSize:z,sortBy:V,filters:H}}=(0,_.useTable)({columns:v,count:a,data:n,disableFilters:!0,disableSortRemove:!0,initialState:m,manualFilters:!0,manualPagination:!0,manualSortBy:!0,autoResetFilters:!1,pageCount:Math.ceil(a/l)},_.useFilters,_.useSortBy,_.usePagination,_.useRowState,_.useRowSelect),[M,O]=(0,i.useState)(p.filters&&r.length?B(r,p.filters):[]);return(0,i.useEffect)((()=>{r.length&&O(B(r,p.filters?p.filters:{}))}),[r]),(0,i.useEffect)((()=>{const t={};M.forEach((e=>{if(void 0!==e.value&&("string"!=typeof e.value||e.value.length>0)){const n=e.urlDisplay||e.id;t[n]=e.value}}));const n={filters:Object.keys(t).length?t:void 0,pageIndex:E};V[0]&&(n.sortColumn=V[0].id,n.sortOrder=V[0].desc?"desc":"asc"),c&&(n.viewMode=b);const a=void 0!==p.pageIndex&&n.pageIndex!==p.pageIndex?"push":"replace";g(n,a),e({pageIndex:E,pageSize:z,sortBy:V,filters:H})}),[e,E,z,V,H]),(0,i.useEffect)((()=>{T()(m.pageIndex,E)||I(m.pageIndex)}),[p]),{canNextPage:k,canPreviousPage:Y,getTableBodyProps:x,getTableProps:y,gotoPage:I,headerGroups:w,pageCount:$,prepareRow:C,rows:S,selectedFlatRows:N,setAllFilters:F,setSortBy:D,state:{pageIndex:E,pageSize:z,sortBy:V,filters:H,internalFilters:M,viewMode:b},toggleAllRowsSelected:R,applyFilterValue:(e,t)=>{O((n=>{if(n[e].value===t)return n;const a={...n[e],value:t},l=function(e,t,n){const a=e.find(((e,n)=>t===n));return[...e.slice(0,t),{...a,...n},...e.slice(t+1)]}(n,e,a);return F(l.filter((e=>!(void 0===e.value||Array.isArray(e.value)&&!e.value.length))).map((({value:e,operator:t,id:n})=>"between"===t&&Array.isArray(e)?[{value:e[0],operator:"gt",id:n},{value:e[1],operator:"lt",id:n}]:{value:e,operator:t,id:n})).flat()),I(0),l}))},setViewMode:f,query:p}}({bulkSelectColumnConfig:he,bulkSelectMode:b&&Boolean(m.length),columns:e,count:n,data:t,fetchData:r,initialPageSize:a,initialSort:c,initialFilters:h,renderCard:Boolean(x),defaultViewMode:k}),le=N&&D,ie=Boolean(h.length);if(ie){const t=e.reduce(((e,t)=>({...e,[t.id||t.accessor]:!0})),{});h.forEach((e=>{if(!t[e.id])throw new R(`Invalid filter config, ${e.id} is not present in columns`)}))}const re=(0,i.useRef)(null),oe=(0,i.useCallback)((()=>{var e;ae.filters&&(null==(e=re.current)||e.clearFilters())}),[ae.filters]),de=Boolean(x),[me,ve]=(0,i.useState)(!1);return(0,i.useEffect)((()=>{b||Q(!1)}),[b,Q]),(0,i.useEffect)((()=>{!s&&J>j-1&&j>0&&G(0)}),[G,s,j,J]),(0,y.FD)(pe,{children:[le&&(0,y.Y)(w,{show:me,selected:K,refreshData:o,resourceName:N,addSuccessToast:E,addDangerToast:z,onHide:()=>ve(!1)}),(0,y.FD)("div",{"data-test":u,className:`superset-list-view ${u}`,children:[(0,y.FD)("div",{className:"header",children:[de&&(0,y.Y)(fe,{mode:ne,setMode:X}),(0,y.FD)("div",{className:"controls","data-test":"filters-select",children:[ie&&(0,y.Y)(se,{ref:re,filters:h,internalFilters:ee,updateFilterValue:q}),"card"===ne&&C&&(0,y.Y)(ce,{initialSort:te,onChange:e=>W(e),options:C})]})]}),(0,y.FD)("div",{className:"body "+(0===O.length?"empty":""),children:[b&&(0,y.Y)(ge,{"data-test":"bulk-select-controls",type:"info",closable:!0,showIcon:!1,onClose:f,message:(0,y.FD)(y.FK,{children:[(0,y.Y)("div",{className:"selectedCopy","data-test":"bulk-select-copy",children:v(K)}),Boolean(K.length)&&(0,y.FD)(y.FK,{children:[(0,y.Y)("span",{"data-test":"bulk-select-deselect-all",role:"button",tabIndex:0,className:"deselect-all",onClick:()=>Q(!1),children:(0,l.t)("Deselect all")}),(0,y.Y)("div",{className:"divider"}),m.map((e=>(0,y.Y)(d.A,{"data-test":"bulk-select-action",buttonStyle:e.type,cta:!0,onClick:()=>e.onSelect(K.map((e=>e.original))),children:e.name},e.key))),D&&(0,y.Y)("span",{"data-test":"bulk-select-tag-btn",role:"button",tabIndex:0,className:"tag-btn",onClick:()=>ve(!0),children:(0,l.t)("Add Tag")})]})]})}),"card"===ne&&(0,y.Y)(Y,{bulkSelectEnabled:b,prepareRow:L,renderCard:x,rows:O,loading:s,showThumbnails:S}),"table"===ne&&(0,y.Y)(g.A,{getTableProps:V,getTableBodyProps:H,prepareRow:L,headerGroups:M,rows:O,columns:e,loading:s,highlightRowId:$,columnsForWrapText:F}),!s&&0===O.length&&(0,y.Y)(be,{className:ne,"data-test":"empty-state",children:ae.filters?(0,y.Y)(ue.p,{title:(0,l.t)("No results match your filter criteria"),description:(0,l.t)("Try different criteria to display results."),size:"large",image:"filter-results.svg",buttonAction:()=>oe(),buttonText:(0,l.t)("clear all filters")}):(0,y.Y)(ue.p,{...I,title:(null==I?void 0:I.title)||(0,l.t)("No Data"),size:"large",image:(null==I?void 0:I.image)||"filter-results.svg"})})]})]}),O.length>0&&(0,y.FD)("div",{className:"pagination-container",children:[(0,y.Y)(p.A,{totalPages:j||0,currentPage:j&&J<j?J+1:0,onChange:e=>G(e-1),hideFirstAndLastPageLinks:!0}),(0,y.Y)("div",{className:"row-count-container",children:!s&&(0,l.t)("%s-%s of %s",Z*J+(O.length&&1),Z*J+O.length,n)})]})]})};var ye;!function(e){e.StartsWith="sw",e.EndsWith="ew",e.Contains="ct",e.Equals="eq",e.NotStartsWith="nsw",e.NotEndsWith="new",e.NotContains="nct",e.NotEquals="neq",e.GreaterThan="gt",e.LessThan="lt",e.RelationManyMany="rel_m_m",e.RelationOneMany="rel_o_m",e.TitleOrSlug="title_or_slug",e.NameOrDescription="name_or_description",e.AllText="all_text",e.ChartAllText="chart_all_text",e.DatasetIsNullOrEmpty="dataset_is_null_or_empty",e.Between="between",e.DashboardIsFav="dashboard_is_favorite",e.ChartIsFav="chart_is_favorite",e.ChartIsCertified="chart_is_certified",e.DashboardIsCertified="dashboard_is_certified",e.DatasetIsCertified="dataset_is_certified",e.DashboardHasCreatedBy="dashboard_has_created_by",e.ChartHasCreatedBy="chart_has_created_by",e.DashboardTagByName="dashboard_tags",e.DashboardTagById="dashboard_tag_id",e.ChartTagByName="chart_tags",e.ChartTagById="chart_tag_id",e.SavedQueryTagByName="saved_query_tags",e.SavedQueryTagById="saved_query_tag_id"}(ye||(ye={}))},47251:(e,t,n)=>{n.d(t,{A:()=>u});var a=n(96453),l=n(46942),i=n.n(l),r=n(2445);const o=a.I4.ul`
  display: inline-block;
  margin: 16px 0;
  padding: 0;

  li {
    display: inline;
    margin: 0 4px;

    span {
      padding: 8px 12px;
      text-decoration: none;
      background-color: ${({theme:e})=>e.colors.grayscale.light5};
      border-radius: ${({theme:e})=>e.borderRadius}px;

      &:hover,
      &:focus {
        z-index: 2;
        color: ${({theme:e})=>e.colors.grayscale.dark1};
        background-color: ${({theme:e})=>e.colors.grayscale.light3};
      }
    }

    &.disabled {
      span {
        background-color: transparent;
        cursor: default;

        &:focus {
          outline: none;
        }
      }
    }
    &.active {
      span {
        z-index: 3;
        color: ${({theme:e})=>e.colors.grayscale.light5};
        cursor: default;
        background-color: ${({theme:e})=>e.colors.primary.base};

        &:focus {
          outline: none;
        }
      }
    }
  }
`;function s({children:e}){return(0,r.Y)(o,{role:"navigation",children:e})}s.Next=function({disabled:e,onClick:t}){return(0,r.Y)("li",{className:i()({disabled:e}),children:(0,r.Y)("span",{role:"button",tabIndex:e?-1:0,onClick:n=>{n.preventDefault(),e||t(n)},children:"»"})})},s.Prev=function({disabled:e,onClick:t}){return(0,r.Y)("li",{className:i()({disabled:e}),children:(0,r.Y)("span",{role:"button",tabIndex:e?-1:0,onClick:n=>{n.preventDefault(),e||t(n)},children:"«"})})},s.Item=function({active:e,children:t,onClick:n}){return(0,r.Y)("li",{className:i()({active:e}),children:(0,r.Y)("span",{role:"button",tabIndex:e?-1:0,onClick:t=>{t.preventDefault(),e||n(t)},children:t})})},s.Ellipsis=function({disabled:e,onClick:t}){return(0,r.Y)("li",{className:i()({disabled:e}),children:(0,r.Y)("span",{role:"button",tabIndex:e?-1:0,onClick:n=>{n.preventDefault(),e||t(n)},children:"…"})})};const d=s;var c=n(18575);const u=(0,c.uv)({WrapperComponent:d,itemTypeToComponent:{[c.w$.PAGE]:({value:e,isActive:t,onClick:n})=>(0,r.Y)(d.Item,{active:t,onClick:n,children:e}),[c.w$.ELLIPSIS]:({isActive:e,onClick:t})=>(0,r.Y)(d.Ellipsis,{disabled:e,onClick:t}),[c.w$.PREVIOUS_PAGE_LINK]:({isActive:e,onClick:t})=>(0,r.Y)(d.Prev,{disabled:e,onClick:t}),[c.w$.NEXT_PAGE_LINK]:({isActive:e,onClick:t})=>(0,r.Y)(d.Next,{disabled:e,onClick:t}),[c.w$.FIRST_PAGE_LINK]:()=>null,[c.w$.LAST_PAGE_LINK]:()=>null}})},73204:(e,t,n)=>{n.d(t,{A:()=>c});var a=n(96540),l=n(46942),i=n.n(l),r=n(96453),o=n(67073),s=n(2445);const d=r.I4.table`
  ${({theme:e})=>`\n    background-color: ${e.colors.grayscale.light5};\n    border-collapse: separate;\n    border-radius: ${e.borderRadius}px;\n\n    thead > tr > th {\n      border: 0;\n    }\n\n    tbody {\n      tr:first-of-type > td {\n        border-top: 0;\n      }\n    }\n    th {\n      background: ${e.colors.grayscale.light5};\n      position: sticky;\n      top: 0;\n\n      &:first-of-type {\n        padding-left: ${4*e.gridUnit}px;\n      }\n\n      &.xs {\n        min-width: 25px;\n      }\n      &.sm {\n        min-width: 50px;\n      }\n      &.md {\n        min-width: 75px;\n      }\n      &.lg {\n        min-width: 100px;\n      }\n      &.xl {\n        min-width: 150px;\n      }\n      &.xxl {\n        min-width: 200px;\n      }\n\n      span {\n        white-space: nowrap;\n        display: flex;\n        align-items: center;\n        line-height: 2;\n      }\n\n      svg {\n        display: inline-block;\n        position: relative;\n      }\n    }\n\n    td {\n      &.xs {\n        width: 25px;\n      }\n      &.sm {\n        width: 50px;\n      }\n      &.md {\n        width: 75px;\n      }\n      &.lg {\n        width: 100px;\n      }\n      &.xl {\n        width: 150px;\n      }\n      &.xxl {\n        width: 200px;\n      }\n    }\n\n    .table-cell-loader {\n      position: relative;\n\n      .loading-bar {\n        background-color: ${e.colors.secondary.light4};\n        border-radius: 7px;\n\n        span {\n          visibility: hidden;\n        }\n      }\n\n      .empty-loading-bar {\n        display: inline-block;\n        width: 100%;\n        height: 1.2em;\n      }\n    }\n\n    .actions {\n      white-space: nowrap;\n      min-width: 100px;\n\n      svg,\n      i {\n        margin-right: 8px;\n\n        &:hover {\n          path {\n            fill: ${e.colors.primary.base};\n          }\n        }\n      }\n    }\n\n    .table-row {\n      .actions {\n        opacity: 0;\n        font-size: ${e.typography.sizes.xl}px;\n        display: flex;\n      }\n\n      &:hover {\n        background-color: ${e.colors.secondary.light5};\n\n        .actions {\n          opacity: 1;\n          transition: opacity ease-in ${e.transitionTiming}s;\n        }\n      }\n    }\n\n    .table-row-selected {\n      background-color: ${e.colors.secondary.light4};\n\n      &:hover {\n        background-color: ${e.colors.secondary.light4};\n      }\n    }\n\n    .table-cell {\n      font-feature-settings: 'tnum' 1;\n      text-overflow: ellipsis;\n      overflow: hidden;\n      max-width: 320px;\n      line-height: 1;\n      vertical-align: middle;\n      &:first-of-type {\n        padding-left: ${4*e.gridUnit}px;\n      }\n      &__wrap {\n        white-space: normal;\n      }\n      &__nowrap {\n        white-space: nowrap;\n      }\n    }\n\n    @keyframes loading-shimmer {\n      40% {\n        background-position: 100% 0;\n      }\n\n      100% {\n        background-position: 100% 0;\n      }\n    }\n  `}
`;d.displayName="table";const c=(0,a.memo)((({getTableProps:e,getTableBodyProps:t,prepareRow:n,headerGroups:a,columns:l,rows:r,loading:c,highlightRowId:u,columnsForWrapText:p})=>(0,s.FD)(d,{...e(),className:"table table-hover","data-test":"listview-table",children:[(0,s.Y)("thead",{children:a.map((e=>(0,s.Y)("tr",{...e.getHeaderGroupProps(),children:e.headers.map((e=>{let t=(0,s.Y)(o.F.Sort,{});return e.isSorted&&e.isSortedDesc?t=(0,s.Y)(o.F.SortDesc,{}):e.isSorted&&!e.isSortedDesc&&(t=(0,s.Y)(o.F.SortAsc,{})),e.hidden?null:(0,s.Y)("th",{...e.getHeaderProps(e.canSort?e.getSortByToggleProps():{}),"data-test":"sort-header",className:i()({[e.size||""]:e.size}),children:(0,s.FD)("span",{children:[e.render("Header"),e.canSort&&t]})})}))})))}),(0,s.FD)("tbody",{...t(),children:[c&&0===r.length&&[...new Array(12)].map(((e,t)=>(0,s.Y)("tr",{children:l.map(((e,t)=>e.hidden?null:(0,s.Y)("td",{className:i()("table-cell",{"table-cell-loader":c}),children:(0,s.Y)("span",{className:"loading-bar empty-loading-bar",role:"progressbar","aria-label":"loading"})},t)))},t))),r.length>0&&r.map((e=>{n(e);const t=e.original.id;return(0,s.Y)("tr",{"data-test":"table-row",...e.getRowProps(),className:i()("table-row",{"table-row-selected":e.isSelected||void 0!==t&&t===u}),children:e.cells.map((e=>{if(e.column.hidden)return null;const t=e.column.cellProps||{},n=null==p?void 0:p.includes(e.column.Header);return(0,s.Y)("td",{"data-test":"table-row-cell",className:i()("table-cell table-cell__"+(n?"wrap":"nowrap"),{"table-cell-loader":c,[e.column.size||""]:e.column.size}),...e.getCellProps(),...t,children:(0,s.Y)("span",{className:i()({"loading-bar":c}),role:c?"progressbar":void 0,children:(0,s.Y)("span",{"data-test":"cell-text",children:e.render("Cell")})})})}))})}))]})]})))}}]);