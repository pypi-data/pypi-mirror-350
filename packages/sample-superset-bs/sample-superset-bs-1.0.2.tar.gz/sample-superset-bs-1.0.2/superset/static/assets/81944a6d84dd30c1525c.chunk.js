"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[217],{47251:(n,e,t)=>{t.d(e,{A:()=>p});var l=t(96453),a=t(46942),i=t.n(a),o=t(2445);const r=l.I4.ul`
  display: inline-block;
  margin: 16px 0;
  padding: 0;

  li {
    display: inline;
    margin: 0 4px;

    span {
      padding: 8px 12px;
      text-decoration: none;
      background-color: ${({theme:n})=>n.colors.grayscale.light5};
      border-radius: ${({theme:n})=>n.borderRadius}px;

      &:hover,
      &:focus {
        z-index: 2;
        color: ${({theme:n})=>n.colors.grayscale.dark1};
        background-color: ${({theme:n})=>n.colors.grayscale.light3};
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
        color: ${({theme:n})=>n.colors.grayscale.light5};
        cursor: default;
        background-color: ${({theme:n})=>n.colors.primary.base};

        &:focus {
          outline: none;
        }
      }
    }
  }
`;function s({children:n}){return(0,o.Y)(r,{role:"navigation",children:n})}s.Next=function({disabled:n,onClick:e}){return(0,o.Y)("li",{className:i()({disabled:n}),children:(0,o.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:t=>{t.preventDefault(),n||e(t)},children:"»"})})},s.Prev=function({disabled:n,onClick:e}){return(0,o.Y)("li",{className:i()({disabled:n}),children:(0,o.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:t=>{t.preventDefault(),n||e(t)},children:"«"})})},s.Item=function({active:n,children:e,onClick:t}){return(0,o.Y)("li",{className:i()({active:n}),children:(0,o.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:e=>{e.preventDefault(),n||t(e)},children:e})})},s.Ellipsis=function({disabled:n,onClick:e}){return(0,o.Y)("li",{className:i()({disabled:n}),children:(0,o.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:t=>{t.preventDefault(),n||e(t)},children:"…"})})};const d=s;var c=t(18575);const p=(0,c.uv)({WrapperComponent:d,itemTypeToComponent:{[c.w$.PAGE]:({value:n,isActive:e,onClick:t})=>(0,o.Y)(d.Item,{active:e,onClick:t,children:n}),[c.w$.ELLIPSIS]:({isActive:n,onClick:e})=>(0,o.Y)(d.Ellipsis,{disabled:n,onClick:e}),[c.w$.PREVIOUS_PAGE_LINK]:({isActive:n,onClick:e})=>(0,o.Y)(d.Prev,{disabled:n,onClick:e}),[c.w$.NEXT_PAGE_LINK]:({isActive:n,onClick:e})=>(0,o.Y)(d.Next,{disabled:n,onClick:e}),[c.w$.FIRST_PAGE_LINK]:()=>null,[c.w$.LAST_PAGE_LINK]:()=>null}})},50217:(n,e,t)=>{t.d(e,{A:()=>l.A,V:()=>l.V});var l=t(54016)},54016:(n,e,t)=>{t.d(e,{A:()=>w,V:()=>l});var l,a=t(2404),i=t.n(a),o=t(96540),r=t(96453),s=t(78518),d=t(32885),c=t(641),p=t(47251),g=t(73204),h=t(2445);!function(n){n.Default="Default",n.Small="Small"}(l||(l={}));const u=r.I4.div`
  margin: ${({theme:n})=>40*n.gridUnit}px 0;
`,m=r.I4.div`
  ${({scrollTable:n,theme:e})=>n&&`\n    flex: 1 1 auto;\n    margin-bottom: ${4*e.gridUnit}px;\n    overflow: auto;\n  `}

  .table-row {
    ${({theme:n,small:e})=>!e&&`height: ${11*n.gridUnit-1}px;`}

    .table-cell {
      ${({theme:n,small:e})=>e&&`\n        padding-top: ${n.gridUnit+1}px;\n        padding-bottom: ${n.gridUnit+1}px;\n        line-height: 1.45;\n      `}
    }
  }

  th[role='columnheader'] {
    z-index: 1;
    border-bottom: ${({theme:n})=>`${n.gridUnit-2}px solid ${n.colors.grayscale.light2}`};
    ${({small:n})=>n&&"padding-bottom: 0;"}
  }
`,b=r.I4.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: ${({theme:n})=>n.colors.grayscale.light5};

  ${({isPaginationSticky:n})=>n&&"\n        position: sticky;\n        bottom: 0;\n        left: 0;\n    "};

  .row-count-container {
    margin-top: ${({theme:n})=>2*n.gridUnit}px;
    color: ${({theme:n})=>n.colors.grayscale.base};
  }
`,x=({columns:n,data:e,pageSize:t,totalCount:a=e.length,initialPageIndex:r,initialSortBy:x=[],loading:w=!1,withPagination:y=!0,emptyWrapperType:f=l.Default,noDataText:v,showRowCount:k=!0,serverPagination:$=!1,columnsForWrapText:P,onServerPagination:S=()=>{},scrollTopOnPagination:Y=!1,...I})=>{const C={pageSize:null!=t?t:10,pageIndex:null!=r?r:0,sortBy:x},{getTableProps:T,getTableBodyProps:N,headerGroups:A,page:E,rows:D,prepareRow:_,pageCount:F,gotoPage:z,state:{pageIndex:R,pageSize:B,sortBy:G}}=(0,d.useTable)({columns:n,data:e,initialState:C,manualPagination:$,manualSortBy:$,pageCount:Math.ceil(a/C.pageSize)},d.useFilters,d.useSortBy,d.usePagination),L=y?E:D;let U;switch(f){case l.Small:U=({children:n})=>(0,h.Y)(h.FK,{children:n});break;case l.Default:default:U=({children:n})=>(0,h.Y)(u,{children:n})}const K=!w&&0===L.length,M=F>1&&y,W=(0,o.useRef)(null);return(0,o.useEffect)((()=>{$&&R!==C.pageIndex&&S({pageIndex:R})}),[R]),(0,o.useEffect)((()=>{$&&!i()(G,C.sortBy)&&S({pageIndex:0,sortBy:G})}),[G]),(0,h.FD)(h.FK,{children:[(0,h.FD)(m,{...I,ref:W,children:[(0,h.Y)(g.A,{getTableProps:T,getTableBodyProps:N,prepareRow:_,headerGroups:A,rows:L,columns:n,loading:w,columnsForWrapText:P}),K&&(0,h.Y)(U,{children:v?(0,h.Y)(c.S,{image:c.S.PRESENTED_IMAGE_SIMPLE,description:v}):(0,h.Y)(c.S,{image:c.S.PRESENTED_IMAGE_SIMPLE})})]}),M&&(0,h.FD)(b,{className:"pagination-container",isPaginationSticky:I.isPaginationSticky,children:[(0,h.Y)(p.A,{totalPages:F||0,currentPage:F?R+1:0,onChange:n=>(n=>{var e;Y&&(null==W||null==(e=W.current)||e.scroll(0,0)),z(n)})(n-1),hideFirstAndLastPageLinks:!0}),k&&(0,h.Y)("div",{className:"row-count-container",children:!w&&(0,s.t)("%s-%s of %s",B*R+(E.length&&1),B*R+E.length,a)})]})]})},w=(0,o.memo)(x)},73204:(n,e,t)=>{t.d(e,{A:()=>c});var l=t(96540),a=t(46942),i=t.n(a),o=t(96453),r=t(67073),s=t(2445);const d=o.I4.table`
  ${({theme:n})=>`\n    background-color: ${n.colors.grayscale.light5};\n    border-collapse: separate;\n    border-radius: ${n.borderRadius}px;\n\n    thead > tr > th {\n      border: 0;\n    }\n\n    tbody {\n      tr:first-of-type > td {\n        border-top: 0;\n      }\n    }\n    th {\n      background: ${n.colors.grayscale.light5};\n      position: sticky;\n      top: 0;\n\n      &:first-of-type {\n        padding-left: ${4*n.gridUnit}px;\n      }\n\n      &.xs {\n        min-width: 25px;\n      }\n      &.sm {\n        min-width: 50px;\n      }\n      &.md {\n        min-width: 75px;\n      }\n      &.lg {\n        min-width: 100px;\n      }\n      &.xl {\n        min-width: 150px;\n      }\n      &.xxl {\n        min-width: 200px;\n      }\n\n      span {\n        white-space: nowrap;\n        display: flex;\n        align-items: center;\n        line-height: 2;\n      }\n\n      svg {\n        display: inline-block;\n        position: relative;\n      }\n    }\n\n    td {\n      &.xs {\n        width: 25px;\n      }\n      &.sm {\n        width: 50px;\n      }\n      &.md {\n        width: 75px;\n      }\n      &.lg {\n        width: 100px;\n      }\n      &.xl {\n        width: 150px;\n      }\n      &.xxl {\n        width: 200px;\n      }\n    }\n\n    .table-cell-loader {\n      position: relative;\n\n      .loading-bar {\n        background-color: ${n.colors.secondary.light4};\n        border-radius: 7px;\n\n        span {\n          visibility: hidden;\n        }\n      }\n\n      .empty-loading-bar {\n        display: inline-block;\n        width: 100%;\n        height: 1.2em;\n      }\n    }\n\n    .actions {\n      white-space: nowrap;\n      min-width: 100px;\n\n      svg,\n      i {\n        margin-right: 8px;\n\n        &:hover {\n          path {\n            fill: ${n.colors.primary.base};\n          }\n        }\n      }\n    }\n\n    .table-row {\n      .actions {\n        opacity: 0;\n        font-size: ${n.typography.sizes.xl}px;\n        display: flex;\n      }\n\n      &:hover {\n        background-color: ${n.colors.secondary.light5};\n\n        .actions {\n          opacity: 1;\n          transition: opacity ease-in ${n.transitionTiming}s;\n        }\n      }\n    }\n\n    .table-row-selected {\n      background-color: ${n.colors.secondary.light4};\n\n      &:hover {\n        background-color: ${n.colors.secondary.light4};\n      }\n    }\n\n    .table-cell {\n      font-feature-settings: 'tnum' 1;\n      text-overflow: ellipsis;\n      overflow: hidden;\n      max-width: 320px;\n      line-height: 1;\n      vertical-align: middle;\n      &:first-of-type {\n        padding-left: ${4*n.gridUnit}px;\n      }\n      &__wrap {\n        white-space: normal;\n      }\n      &__nowrap {\n        white-space: nowrap;\n      }\n    }\n\n    @keyframes loading-shimmer {\n      40% {\n        background-position: 100% 0;\n      }\n\n      100% {\n        background-position: 100% 0;\n      }\n    }\n  `}
`;d.displayName="table";const c=(0,l.memo)((({getTableProps:n,getTableBodyProps:e,prepareRow:t,headerGroups:l,columns:a,rows:o,loading:c,highlightRowId:p,columnsForWrapText:g})=>(0,s.FD)(d,{...n(),className:"table table-hover","data-test":"listview-table",children:[(0,s.Y)("thead",{children:l.map((n=>(0,s.Y)("tr",{...n.getHeaderGroupProps(),children:n.headers.map((n=>{let e=(0,s.Y)(r.F.Sort,{});return n.isSorted&&n.isSortedDesc?e=(0,s.Y)(r.F.SortDesc,{}):n.isSorted&&!n.isSortedDesc&&(e=(0,s.Y)(r.F.SortAsc,{})),n.hidden?null:(0,s.Y)("th",{...n.getHeaderProps(n.canSort?n.getSortByToggleProps():{}),"data-test":"sort-header",className:i()({[n.size||""]:n.size}),children:(0,s.FD)("span",{children:[n.render("Header"),n.canSort&&e]})})}))})))}),(0,s.FD)("tbody",{...e(),children:[c&&0===o.length&&[...new Array(12)].map(((n,e)=>(0,s.Y)("tr",{children:a.map(((n,e)=>n.hidden?null:(0,s.Y)("td",{className:i()("table-cell",{"table-cell-loader":c}),children:(0,s.Y)("span",{className:"loading-bar empty-loading-bar",role:"progressbar","aria-label":"loading"})},e)))},e))),o.length>0&&o.map((n=>{t(n);const e=n.original.id;return(0,s.Y)("tr",{"data-test":"table-row",...n.getRowProps(),className:i()("table-row",{"table-row-selected":n.isSelected||void 0!==e&&e===p}),children:n.cells.map((n=>{if(n.column.hidden)return null;const e=n.column.cellProps||{},t=null==g?void 0:g.includes(n.column.Header);return(0,s.Y)("td",{"data-test":"table-row-cell",className:i()("table-cell table-cell__"+(t?"wrap":"nowrap"),{"table-cell-loader":c,[n.column.size||""]:n.column.size}),...n.getCellProps(),...e,children:(0,s.Y)("span",{className:i()({"loading-bar":c}),role:c?"progressbar":void 0,children:(0,s.Y)("span",{"data-test":"cell-text",children:n.render("Cell")})})})}))})}))]})]})))}}]);