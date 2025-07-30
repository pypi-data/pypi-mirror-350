"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3463],{641:(e,t,r)=>{r.d(t,{S:()=>a});var l=r(99494),i=r(2445);const a=Object.assign((e=>(0,i.Y)(l.A,{...e})),{PRESENTED_IMAGE_SIMPLE:l.A.PRESENTED_IMAGE_SIMPLE,PRESENTED_IMAGE_DEFAULT:l.A.PRESENTED_IMAGE_DEFAULT})},888:(e,t,r)=>{r.d(t,{A:()=>fe});var l=r(96540),i=r(96453),a=r(18301),n=r(61225),o=r(82960),s=r(78130),c=r(72173),d=r(5556),h=r.n(d),p=r(46942),u=r.n(p),m=r(46920),v=r(17437),f=r(78518),g=r(62193),b=r.n(g),y=r(81151),x=r(49588);const w=[x.B8,x.tq];function z({currentNode:e={},components:t={},filterFields:r=[],selectedChartId:l}){if(!e)return null;const{type:i}=e;if(x.oT===i&&e&&e.meta&&e.meta.chartId)return{value:e.meta.chartId,label:e.meta.sliceName||`${i} ${e.meta.chartId}`,type:i,showCheckbox:l!==e.meta.chartId,children:[]};let a=[];if(e.children&&e.children.length&&e.children.forEach((e=>{const i=z({currentNode:t[e],components:t,filterFields:r,selectedChartId:l}),n=t[e].type;w.includes(n)?a.push(i):a=a.concat(i)})),w.includes(i)){let t=null;return t=i===x.tq?(0,f.t)("All charts"):e.meta&&e.meta.text?e.meta.text:`${i} ${e.id}`,{value:e.id,label:t,type:i,children:a}}return a}function C({components:e={},filterFields:t=[],selectedChartId:r}){return b()(e)?[]:[{...z({currentNode:e[y.wv],components:e,filterFields:t,selectedChartId:r})}]}function F(e=[],t=-1){const r=[],l=(e,i)=>{e&&e.children&&(-1===t||i<t)&&(r.push(e.value),e.children.forEach((e=>l(e,i+1))))};return e.length>0&&e.forEach((e=>{l(e,0)})),r}var k=r(12066);function E({activeFilterField:e,checkedFilterFields:t}){return(0,k.J)(e?[e]:t)}var Y=r(24647);function S({activeFilterField:e,checkedFilterFields:t}){if(e)return(0,Y.w)(e).chartId;if(t.length){const{chartId:e}=(0,Y.w)(t[0]);return t.some((t=>(0,Y.w)(t).chartId!==e))?null:e}return null}function M({checkedFilterFields:e=[],activeFilterField:t,filterScopeMap:r={},layout:l={}}){const i=E({checkedFilterFields:e,activeFilterField:t}),a=t?[t]:e,n=C({components:l,filterFields:a,selectedChartId:S({checkedFilterFields:e,activeFilterField:t})}),o=new Set;a.forEach((e=>{(r[e].checked||[]).forEach((t=>{o.add(`${t}:${e}`)}))}));const s=[...o],c=r[i]?r[i].expanded:F(n,1);return{[i]:{nodes:n,nodesFiltered:[...n],checked:s,expanded:c}}}var $=r(47307),O=r.n($),A=r(89143),V=r.n(A),I=r(8209),H=r.n(I),D=r(89899),N=r.n(D);function _({tabScopes:e,parentNodeValue:t,forceAggregate:r=!1,hasChartSiblings:l=!1,tabChildren:i=[],immuneChartSiblings:a=[]}){if(r||!l&&Object.entries(e).every((([e,{scope:t}])=>t&&t.length&&e===t[0]))){const r=function({tabs:e=[],tabsInScope:t=[]}){const r=[];return e.forEach((({value:e,children:l})=>{l&&!t.includes(e)&&l.forEach((({value:e,children:l})=>{l&&!t.includes(e)&&r.push(...l.filter((({type:e})=>e===x.oT)))}))})),r.map((({value:e})=>e))}({tabs:i,tabsInScope:O()(e,(({scope:e})=>e))}),l=O()(Object.values(e),(({immune:e})=>e));return{scope:[t],immune:[...new Set([...r,...l])]}}const n=Object.values(e).filter((({scope:e})=>e&&e.length));return{scope:O()(n,(({scope:e})=>e)),immune:n.length?O()(n,(({immune:e})=>e)):O()(Object.values(e),(({immune:e})=>e)).concat(a)}}function R({currentNode:e={},filterId:t,checkedChartIds:r=[]}){if(!e)return{};const{value:l,children:i}=e,a=i.filter((({type:e})=>e===x.oT)),n=i.filter((({type:e})=>e===x.B8)),o=a.filter((({value:e})=>t!==e&&!r.includes(e))).map((({value:e})=>e)),s=N()(H()((e=>e.value)),V()((e=>R({currentNode:e,filterId:t,checkedChartIds:r}))))(n);if(!b()(a)&&a.some((({value:e})=>r.includes(e)))){if(b()(n))return{scope:[l],immune:o};const{scope:e,immune:t}=_({tabScopes:s,parentNodeValue:l,forceAggregate:!0,tabChildren:n});return{scope:e,immune:o.concat(t)}}return n.length?_({tabScopes:s,parentNodeValue:l,hasChartSiblings:!b()(a),tabChildren:n,immuneChartSiblings:o}):{scope:[],immune:o}}function U({filterKey:e,nodes:t=[],checkedChartIds:r=[]}){if(t.length){const{chartId:l}=(0,Y.w)(e);return R({currentNode:t[0],filterId:l,checkedChartIds:r})}return{}}var j=r(68921),T=r(4881),L=r(38491),P=r.n(L),B=r(67073),q=r(2445);const W=(0,i.I4)(B.F.BarChartOutlined)`
  ${({theme:e})=>`\n    position: relative;\n    top: ${e.gridUnit-1}px;\n    color: ${e.colors.primary.base};\n    margin-right: ${2*e.gridUnit}px;\n  `}
`;function K({currentNode:e={},selectedChartId:t}){if(!e)return null;const{label:r,value:l,type:i,children:a}=e;if(a&&a.length){const n=a.map((e=>K({currentNode:e,selectedChartId:t})));return{...e,label:(0,q.FD)("span",{className:u()(`filter-scope-type ${i.toLowerCase()}`,{"selected-filter":t===l}),children:[i===x.oT&&(0,q.Y)(W,{}),r]}),children:n}}return{...e,label:(0,q.Y)("span",{className:u()(`filter-scope-type ${i.toLowerCase()}`,{"selected-filter":t===l}),children:r})}}function Z({nodes:e,selectedChartId:t}){return e?e.map((e=>K({currentNode:e,selectedChartId:t}))):[]}var G=r(75264);const J={check:(0,q.Y)(G.Dj,{}),uncheck:(0,q.Y)(G.cp,{}),halfCheck:(0,q.Y)(G.cE,{}),expandClose:(0,q.Y)("span",{className:"rct-icon rct-icon-expand-close"}),expandOpen:(0,q.Y)("span",{className:"rct-icon rct-icon-expand-open"}),expandAll:(0,q.Y)("span",{className:"rct-icon rct-icon-expand-all",children:(0,f.t)("Expand all")}),collapseAll:(0,q.Y)("span",{className:"rct-icon rct-icon-collapse-all",children:(0,f.t)("Collapse all")}),parentClose:(0,q.Y)("span",{className:"rct-icon rct-icon-parent-close"}),parentOpen:(0,q.Y)("span",{className:"rct-icon rct-icon-parent-open"}),leaf:(0,q.Y)("span",{className:"rct-icon rct-icon-leaf"})},Q={nodes:h().arrayOf(T.QU).isRequired,checked:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,expanded:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,onCheck:h().func.isRequired,onExpand:h().func.isRequired,selectedChartId:h().number},X=()=>{};function ee({nodes:e=[],checked:t=[],expanded:r=[],onCheck:l,onExpand:i,selectedChartId:a}){return(0,q.Y)(P(),{showExpandAll:!0,expandOnClick:!0,showNodeIcon:!1,nodes:Z({nodes:e,selectedChartId:a}),checked:t,expanded:r,onCheck:l,onExpand:i,onClick:X,icons:J})}ee.propTypes=Q,ee.defaultProps={selectedChartId:null};var te=r(40563);const re={label:h().string.isRequired,isSelected:h().bool.isRequired};function le({label:e,isSelected:t}){return(0,q.Y)("span",{className:u()("filter-field-item filter-container",{"is-selected":t}),children:(0,q.Y)(te.lR,{htmlFor:e,children:e})})}function ie({nodes:e,activeKey:t}){if(!e)return[];const r=e[0],l=r.children.map((e=>({...e,children:e.children.map((e=>{const{label:r,value:l}=e;return{...e,label:(0,q.Y)(le,{isSelected:l===t,label:r})}}))})));return[{...r,label:(0,q.Y)("span",{className:"root",children:r.label}),children:l}]}le.propTypes=re;const ae={activeKey:h().string,nodes:h().arrayOf(T.QU).isRequired,checked:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,expanded:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,onCheck:h().func.isRequired,onExpand:h().func.isRequired,onClick:h().func.isRequired};function ne({activeKey:e,nodes:t=[],checked:r=[],expanded:l=[],onClick:i,onCheck:a,onExpand:n}){return(0,q.Y)(P(),{showExpandAll:!0,showNodeIcon:!1,expandOnClick:!0,nodes:ie({nodes:t,activeKey:e}),checked:r,expanded:l,onClick:i,onCheck:a,onExpand:n,icons:J})}ne.propTypes=ae,ne.defaultProps={activeKey:null};const oe={dashboardFilters:h().objectOf(T.d2).isRequired,layout:h().object.isRequired,updateDashboardFiltersScope:h().func.isRequired,setUnsavedChanges:h().func.isRequired,onCloseModal:h().func.isRequired},se=i.I4.div`
  ${({theme:e})=>v.AH`
    display: flex;
    flex-direction: column;
    height: 80%;
    margin-right: ${-6*e.gridUnit}px;
    font-size: ${e.typography.sizes.m}px;

    & .nav.nav-tabs {
      border: none;
    }

    & .filter-scope-body {
      flex: 1;
      max-height: calc(100% - ${32*e.gridUnit}px);

      .filter-field-pane,
      .filter-scope-pane {
        overflow-y: auto;
      }
    }

    & .warning-message {
      padding: ${6*e.gridUnit}px;
    }
  `}
`,ce=i.I4.div`
  ${({theme:e})=>v.AH`
    &.filter-scope-body {
      flex: 1;
      max-height: calc(100% - ${32*e.gridUnit}px);

      .filter-field-pane,
      .filter-scope-pane {
        overflow-y: auto;
      }
    }
  `}
`,de=i.I4.div`
  ${({theme:e})=>v.AH`
    height: ${16*e.gridUnit}px;
    border-bottom: 1px solid ${e.colors.grayscale.light2};
    padding-left: ${6*e.gridUnit}px;
    margin-left: ${-6*e.gridUnit}px;

    h4 {
      margin-top: 0;
    }

    .selected-fields {
      margin: ${3*e.gridUnit}px 0 ${4*e.gridUnit}px;
      visibility: hidden;

      &.multi-edit-mode {
        visibility: visible;
      }

      .selected-scopes {
        padding-left: ${e.gridUnit}px;
      }
    }
  `}
`,he=i.I4.div`
  ${({theme:e})=>v.AH`
    &.filters-scope-selector {
      display: flex;
      flex-direction: row;
      position: relative;
      height: 100%;

      a,
      a:active,
      a:hover {
        color: inherit;
        text-decoration: none;
      }

      .react-checkbox-tree .rct-icon.rct-icon-expand-all,
      .react-checkbox-tree .rct-icon.rct-icon-collapse-all {
        font-family: ${e.typography.families.sansSerif};
        font-size: ${e.typography.sizes.m}px;
        color: ${e.colors.primary.base};

        &::before {
          content: '';
        }

        &:hover {
          text-decoration: underline;
        }

        &:focus {
          outline: none;
        }
      }

      .filter-field-pane {
        position: relative;
        width: 40%;
        padding: ${4*e.gridUnit}px;
        padding-left: 0;
        border-right: 1px solid ${e.colors.grayscale.light2};

        .filter-container label {
          font-weight: ${e.typography.weights.normal};
          margin: 0 0 0 ${4*e.gridUnit}px;
          word-break: break-all;
        }

        .filter-field-item {
          height: ${9*e.gridUnit}px;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0 ${6*e.gridUnit}px;
          margin-left: ${-6*e.gridUnit}px;

          &.is-selected {
            border: 1px solid ${e.colors.text.label};
            border-radius: ${e.borderRadius}px;
            background-color: ${e.colors.grayscale.light4};
            margin-left: ${-6*e.gridUnit}px;
          }
        }

        .react-checkbox-tree {
          .rct-title .root {
            font-weight: ${e.typography.weights.bold};
          }

          .rct-text {
            height: ${10*e.gridUnit}px;
          }
        }
      }

      .filter-scope-pane {
        position: relative;
        flex: 1;
        padding: ${4*e.gridUnit}px;
        padding-right: ${6*e.gridUnit}px;
      }

      .react-checkbox-tree {
        flex-direction: column;
        color: ${e.colors.grayscale.dark1};
        font-size: ${e.typography.sizes.m}px;

        .filter-scope-type {
          padding: ${2*e.gridUnit}px 0;
          display: flex;
          align-items: center;

          &.chart {
            font-weight: ${e.typography.weights.normal};
          }

          &.selected-filter {
            padding-left: ${7*e.gridUnit}px;
            position: relative;
            color: ${e.colors.text.label};

            &::before {
              content: ' ';
              position: absolute;
              left: 0;
              top: 50%;
              width: ${4*e.gridUnit}px;
              height: ${4*e.gridUnit}px;
              border-radius: ${e.borderRadius}px;
              margin-top: ${-2*e.gridUnit}px;
              box-shadow: inset 0 0 0 2px ${e.colors.grayscale.light2};
              background: ${e.colors.grayscale.light3};
            }
          }

          &.root {
            font-weight: ${e.typography.weights.bold};
          }
        }

        .rct-checkbox {
          svg {
            position: relative;
            top: 3px;
            width: ${4.5*e.gridUnit}px;
          }
        }

        .rct-node-leaf {
          .rct-bare-label {
            &::before {
              padding-left: ${e.gridUnit}px;
            }
          }
        }

        .rct-options {
          text-align: left;
          margin-left: 0;
          margin-bottom: ${2*e.gridUnit}px;
        }

        .rct-text {
          margin: 0;
          display: flex;
        }

        .rct-title {
          display: block;
        }

        // disable style from react-checkbox-trees.css
        .rct-node-clickable:hover,
        .rct-node-clickable:focus,
        label:hover,
        label:active {
          background: none !important;
        }
      }

      .multi-edit-mode {
        .filter-field-item {
          padding: 0 ${4*e.gridUnit}px 0 ${12*e.gridUnit}px;
          margin-left: ${-12*e.gridUnit}px;

          &.is-selected {
            margin-left: ${-13*e.gridUnit}px;
          }
        }
      }

      .scope-search {
        position: absolute;
        right: ${4*e.gridUnit}px;
        top: ${4*e.gridUnit}px;
        border-radius: ${e.borderRadius}px;
        border: 1px solid ${e.colors.grayscale.light2};
        padding: ${e.gridUnit}px ${2*e.gridUnit}px;
        font-size: ${e.typography.sizes.m}px;
        outline: none;

        &:focus {
          border: 1px solid ${e.colors.primary.base};
        }
      }
    }
  `}
`,pe=i.I4.div`
  ${({theme:e})=>`\n    height: ${16*e.gridUnit}px;\n\n    border-top: ${e.gridUnit/4}px solid ${e.colors.primary.light3};\n    padding: ${6*e.gridUnit}px;\n    margin: 0 0 0 ${6*-e.gridUnit}px;\n    text-align: right;\n\n    .btn {\n      margin-right: ${4*e.gridUnit}px;\n\n      &:last-child {\n        margin-right: 0;\n      }\n    }\n  `}
`;class ue extends l.PureComponent{constructor(e){super(e);const{dashboardFilters:t,layout:r}=e;if(Object.keys(t).length>0){const e=function({dashboardFilters:e={}}){const t=Object.values(e).map((e=>{const{chartId:t,filterName:r,columns:l,labels:i}=e,a=Object.keys(l).map((e=>({value:(0,Y.s)({chartId:t,column:e}),label:i[e]||e})));return{value:t,label:r,children:a,showCheckbox:!0}}));return[{value:y.zf,type:x.tq,label:(0,f.t)("All filters"),children:t}]}({dashboardFilters:t}),l=e[0].children;this.allfilterFields=[],l.forEach((({children:e})=>{e.forEach((e=>{this.allfilterFields.push(e.value)}))})),this.defaultFilterKey=l[0].children[0].value;const i=Object.values(t).reduce(((e,{chartId:l,columns:i})=>({...e,...Object.keys(i).reduce(((e,i)=>{const a=(0,Y.s)({chartId:l,column:i}),n=C({components:r,filterFields:[a],selectedChartId:l}),o=F(n,1),s=((0,j._i)({filterScope:t[l].scopes[i]})||[]).filter((e=>e!==l));return{...e,[a]:{nodes:n,nodesFiltered:[...n],checked:s,expanded:o}}}),{})})),{}),{chartId:a}=(0,Y.w)(this.defaultFilterKey),n=[],o=this.defaultFilterKey,s=[y.zf].concat(a),c=M({checkedFilterFields:n,activeFilterField:o,filterScopeMap:i,layout:r});this.state={showSelector:!0,activeFilterField:o,searchText:"",filterScopeMap:{...i,...c},filterFieldNodes:e,checkedFilterFields:n,expandedFilterIds:s}}else this.state={showSelector:!1};this.filterNodes=this.filterNodes.bind(this),this.onChangeFilterField=this.onChangeFilterField.bind(this),this.onCheckFilterScope=this.onCheckFilterScope.bind(this),this.onExpandFilterScope=this.onExpandFilterScope.bind(this),this.onSearchInputChange=this.onSearchInputChange.bind(this),this.onCheckFilterField=this.onCheckFilterField.bind(this),this.onExpandFilterField=this.onExpandFilterField.bind(this),this.onClose=this.onClose.bind(this),this.onSave=this.onSave.bind(this)}onCheckFilterScope(e=[]){const{activeFilterField:t,filterScopeMap:r,checkedFilterFields:l}=this.state,i=E({activeFilterField:t,checkedFilterFields:l}),a=t?[t]:l,n={...r[i],checked:e},o=function({checked:e=[],filterFields:t=[],filterScopeMap:r={}}){const l=e.reduce(((e,t)=>{const[r,l]=t.split(":");return{...e,[l]:(e[l]||[]).concat(parseInt(r,10))}}),{});return t.reduce(((e,t)=>({...e,[t]:{...r[t],checked:l[t]||[]}})),{})}({checked:e,filterFields:a,filterScopeMap:r});this.setState((()=>({filterScopeMap:{...r,...o,[i]:n}})))}onExpandFilterScope(e=[]){const{activeFilterField:t,checkedFilterFields:r,filterScopeMap:l}=this.state,i=E({activeFilterField:t,checkedFilterFields:r}),a={...l[i],expanded:e};this.setState((()=>({filterScopeMap:{...l,[i]:a}})))}onCheckFilterField(e=[]){const{layout:t}=this.props,{filterScopeMap:r}=this.state,l=M({checkedFilterFields:e,activeFilterField:null,filterScopeMap:r,layout:t});this.setState((()=>({activeFilterField:null,checkedFilterFields:e,filterScopeMap:{...r,...l}})))}onExpandFilterField(e=[]){this.setState((()=>({expandedFilterIds:e})))}onChangeFilterField(e={}){const{layout:t}=this.props,r=e.value,{activeFilterField:l,checkedFilterFields:i,filterScopeMap:a}=this.state;if(r===l){const e=M({checkedFilterFields:i,activeFilterField:null,filterScopeMap:a,layout:t});this.setState({activeFilterField:null,filterScopeMap:{...a,...e}})}else if(this.allfilterFields.includes(r)){const e=M({checkedFilterFields:i,activeFilterField:r,filterScopeMap:a,layout:t});this.setState({activeFilterField:r,filterScopeMap:{...a,...e}})}}onSearchInputChange(e){this.setState({searchText:e.target.value},this.filterTree)}onClose(){this.props.onCloseModal()}onSave(){const{filterScopeMap:e}=this.state,t=this.allfilterFields.reduce(((t,r)=>{const{nodes:l}=e[r],i=e[r].checked;return{...t,[r]:U({filterKey:r,nodes:l,checkedChartIds:i})}}),{});this.props.updateDashboardFiltersScope(t),this.props.setUnsavedChanges(!0),this.props.onCloseModal()}filterTree(){if(this.state.searchText){const e=e=>{const{activeFilterField:t,checkedFilterFields:r,filterScopeMap:l}=e,i=E({activeFilterField:t,checkedFilterFields:r}),a=l[i].nodes.reduce(this.filterNodes,[]),n=F([...a]),o={...l[i],nodesFiltered:a,expanded:n};return{filterScopeMap:{...l,[i]:o}}};this.setState(e)}else this.setState((e=>{const{activeFilterField:t,checkedFilterFields:r,filterScopeMap:l}=e,i=E({activeFilterField:t,checkedFilterFields:r}),a={...l[i],nodesFiltered:l[i].nodes};return{filterScopeMap:{...l,[i]:a}}}))}filterNodes(e=[],t={}){const{searchText:r}=this.state,l=(t.children||[]).reduce(this.filterNodes,[]);return(t.label.toLocaleLowerCase().indexOf(r.toLocaleLowerCase())>-1||l.length)&&e.push({...t,children:l}),e}renderFilterFieldList(){const{activeFilterField:e,filterFieldNodes:t,checkedFilterFields:r,expandedFilterIds:l}=this.state;return(0,q.Y)(ne,{activeKey:e,nodes:t,checked:r,expanded:l,onClick:this.onChangeFilterField,onCheck:this.onCheckFilterField,onExpand:this.onExpandFilterField})}renderFilterScopeTree(){const{filterScopeMap:e,activeFilterField:t,checkedFilterFields:r,searchText:l}=this.state,i=E({activeFilterField:t,checkedFilterFields:r}),a=S({activeFilterField:t,checkedFilterFields:r});return(0,q.FD)(q.FK,{children:[(0,q.Y)("input",{className:"filter-text scope-search multi-edit-mode",placeholder:(0,f.t)("Search..."),type:"text",value:l,onChange:this.onSearchInputChange}),(0,q.Y)(ee,{nodes:e[i].nodesFiltered,checked:e[i].checked,expanded:e[i].expanded,onCheck:this.onCheckFilterScope,onExpand:this.onExpandFilterScope,selectedChartId:a})]})}renderEditingFiltersName(){const{dashboardFilters:e}=this.props,{activeFilterField:t,checkedFilterFields:r}=this.state,l=[].concat(t||r).map((t=>{const{chartId:r,column:l}=(0,Y.w)(t);return e[r].labels[l]||l}));return(0,q.FD)("div",{className:"selected-fields multi-edit-mode",children:[0===l.length&&(0,f.t)("No filter is selected."),1===l.length&&(0,f.t)("Editing 1 filter:"),l.length>1&&(0,f.t)("Batch editing %d filters:",l.length),(0,q.Y)("span",{className:"selected-scopes",children:l.join(", ")})]})}render(){const{showSelector:e}=this.state;return(0,q.FD)(se,{children:[(0,q.FD)(de,{children:[(0,q.Y)("h4",{children:(0,f.t)("Configure filter scopes")}),e&&this.renderEditingFiltersName()]}),(0,q.Y)(ce,{className:"filter-scope-body",children:e?(0,q.FD)(he,{className:"filters-scope-selector",children:[(0,q.Y)("div",{className:u()("filter-field-pane multi-edit-mode"),children:this.renderFilterFieldList()}),(0,q.Y)("div",{className:"filter-scope-pane multi-edit-mode",children:this.renderFilterScopeTree()})]}):(0,q.Y)("div",{className:"warning-message",children:(0,f.t)("There are no filters in this dashboard.")})}),(0,q.FD)(pe,{children:[(0,q.Y)(m.A,{buttonSize:"small",onClick:this.onClose,children:(0,f.t)("Close")}),e&&(0,q.Y)(m.A,{buttonSize:"small",buttonStyle:"primary",onClick:this.onSave,children:(0,f.t)("Save")})]})]})}}ue.propTypes=oe;const me=(0,n.Ng)((function({dashboardLayout:e,dashboardFilters:t}){return{dashboardFilters:t,layout:e.present}}),(function(e){return(0,o.zH)({updateDashboardFiltersScope:s.B8,setUnsavedChanges:c.MR},e)}))(ue),ve=i.I4.div((({theme:{gridUnit:e}})=>({padding:2*e,paddingBottom:3*e})));class fe extends l.PureComponent{constructor(e){super(e),this.modal=void 0,this.modal=(0,l.createRef)(),this.handleCloseModal=this.handleCloseModal.bind(this)}handleCloseModal(){var e,t;null==this||null==(e=this.modal)||null==(t=e.current)||null==t.close||t.close()}render(){const e={onCloseModal:this.handleCloseModal};return(0,q.Y)(a.A,{ref:this.modal,triggerNode:this.props.triggerNode,modalBody:(0,q.Y)(ve,{children:(0,q.Y)(me,{...e})}),width:"80%"})}}},3932:(e,t,r)=>{r.d(t,{m:()=>p});var l=r(35742),i=r(78518),a=r(51436),n=r(58561),o=r.n(n),s=r(43859);const c=new Map,d=(0,s.K)(l.A.get,c,(({endpoint:e})=>e||"")),h=e=>({value:e.id,label:e.name,key:e.id}),p=async(e,t,r)=>{const l="name",n=o().encode({filters:[{col:l,opr:"ct",value:e},{col:"type",opr:"custom_tag",value:!0}],page:t,page_size:r,order_column:l,order_direction:"asc"});return d({endpoint:`/api/v1/tag/?q=${n}`}).then((e=>({data:e.json.result.map(h),totalCount:e.json.count}))).catch((async e=>{const t=(({error:e,message:t})=>{let r=t||e||(0,i.t)("An error has occurred");return"Forbidden"===t&&(r=(0,i.t)("You do not have permission to read tags")),r})(await(0,a.h4)(e));throw new Error(t)}))}},18301:(e,t,r)=>{r.d(t,{A:()=>o});var l=r(96540),i=r(85861),a=r(46920),n=r(2445);const o=(0,l.forwardRef)(((e,t)=>{const[r,o]=(0,l.useState)(!1),{beforeOpen:s=()=>{},onExit:c=()=>{},isButton:d=!1,resizable:h=!1,draggable:p=!1,className:u="",tooltip:m,modalFooter:v,triggerNode:f,destroyOnClose:g=!0,modalBody:b,draggableConfig:y={},resizableConfig:x={},modalTitle:w,responsive:z,width:C,maxWidth:F}=e,k=()=>{o(!1),null==c||c()},E=e=>{e.preventDefault(),null==s||s(),o(!0)};return t&&(t.current={close:k,open:E,showModal:r}),(0,n.FD)(n.FK,{children:[d&&(0,n.Y)(a.A,{className:"modal-trigger","data-test":"btn-modal-trigger",tooltip:m,onClick:E,children:f}),!d&&(0,n.Y)("div",{"data-test":"span-modal-trigger",onClick:E,role:"button",children:f}),(0,n.Y)(i.Ay,{className:u,show:r,onHide:k,title:w,footer:v,hideFooter:!v,width:C,maxWidth:F,responsive:z,resizable:h,resizableConfig:x,draggable:p,draggableConfig:y,destroyOnClose:g,children:b})]})}))},25106:(e,t,r)=>{function l(e){return e?e.full_name||`${e.first_name} ${e.last_name}`:""}r.d(t,{A:()=>l})},29307:(e,t,r)=>{r.d(t,{A:()=>s});var l=r(96540),i=r(96453),a=r(5362),n=r(2445);const o=i.I4.div`
  background-image: url(${({src:e})=>e});
  background-size: cover;
  background-position: center ${({position:e})=>e};
  display: inline-block;
  height: calc(100% - 1px);
  width: calc(100% - 2px);
  margin: 1px 1px 0 1px;
`;function s({src:e,fallback:t,isLoading:r,position:i,...s}){const[c,d]=(0,l.useState)(t);return(0,l.useEffect)((()=>(e&&fetch(e).then((e=>e.blob())).then((e=>{if(/image/.test(e.type)){const t=URL.createObjectURL(e);d(t)}})).catch((e=>{a.A.error(e),d(t)})),()=>{d(t)})),[e,t]),(0,n.Y)(o,{"data-test":"image-loader",src:r?t:c,...s,position:i})}},37020:(e,t,r)=>{r.d(t,{A:()=>p});var l=r(96453),i=r(78518),a=r(96540),n=r(90868),o=r(85861),s=r(40563),c=r(2445);const d=l.I4.div`
  padding-top: 8px;
  width: 50%;
  label {
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,h=l.I4.div`
  line-height: ${({theme:e})=>4*e.gridUnit}px;
  padding-top: 16px;
`;function p({description:e,onConfirm:t,onHide:r,open:l,title:p}){const[u,m]=(0,a.useState)(!0),[v,f]=(0,a.useState)(""),g=()=>{f(""),t()};return(0,c.FD)(o.Ay,{disablePrimaryButton:u,onHide:()=>{f(""),r()},onHandledPrimaryAction:g,primaryButtonName:(0,i.t)("Delete"),primaryButtonType:"danger",show:l,title:p,centered:!0,children:[(0,c.Y)(h,{children:e}),(0,c.FD)(d,{children:[(0,c.Y)(s.lR,{htmlFor:"delete",children:(0,i.t)('Type "%s" to confirm',(0,i.t)("DELETE"))}),(0,c.Y)(n.pd,{"data-test":"delete-modal-input",type:"text",id:"delete",autoComplete:"off",value:v,onChange:e=>{var t;const r=null!=(t=e.target.value)?t:"";m(r.toUpperCase()!==(0,i.t)("DELETE")),f(r)},onPressEnter:()=>{u||g()}})]})]})}},39339:(e,t,r)=>{r.d(t,{u:()=>i});var l=r(38708);function i(e){return`${(0,l.KX)()}${e.startsWith("/")?e:`/${e}`}`}},43859:(e,t,r)=>{r.d(t,{K:()=>l});const l=(e,t,r=(...e)=>JSON.stringify([...e]))=>(...l)=>{const i=r(...l);if(t.has(i))return t.get(i);const a=e(...l);return t.set(i,a),a}},46e3:(e,t,r)=>{r.d(t,{A:()=>s});var l,i,a=r(96540);function n(){return n=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},n.apply(null,arguments)}const o=({title:e,titleId:t,...r},o)=>a.createElement("svg",n({xmlns:"http://www.w3.org/2000/svg",width:160,height:170,fill:"none",viewBox:"0 0 160 166",ref:o,"aria-labelledby":t},r),e?a.createElement("title",{id:t},e):null,l||(l=a.createElement("path",{fill:"currentColor",fillOpacity:.5,fillRule:"evenodd",stroke:"currentColor",d:"M123.638 8a.5.5 0 0 0-.5.5V158h28.758V8.5a.5.5 0 0 0-.5-.5zM84.793 40.643a.5.5 0 0 1 .5-.5h27.759a.5.5 0 0 1 .5.5V158H84.793zM46.95 72.285a.5.5 0 0 0-.5.5V158h28.758V72.785a.5.5 0 0 0-.5-.5zM8.604 93.715a.5.5 0 0 0-.5.5V158h28.758V94.215a.5.5 0 0 0-.5-.5z",clipRule:"evenodd"})),i||(i=a.createElement("path",{fill:"currentColor",fillOpacity:.5,stroke:"currentColor",d:"M123.138 158h-.5v.5h.5zm28.758 0v.5h.5v-.5zm-38.344 0v.5h.5v-.5zm-28.759 0h-.5v.5h.5zm-38.344-.001h-.5v.5h.5zm28.758 0v.5h.5v-.5zM8.104 158h-.5v.5h.5zm28.758 0v.5h.5v-.5zM123.639 8.5v-1a1 1 0 0 0-1 1zm0 149.5V8.5h-1V158zm28.258-.5h-28.758v1h28.758zm-.5-149V158h1V8.5zm0 0h1a1 1 0 0 0-1-1zm-27.758 0h27.758v-1h-27.758zM85.293 39.643a1 1 0 0 0-1 1h1zm27.759 0H85.293v1h27.759zm1 1a1 1 0 0 0-1-1v1zm0 117.357V40.643h-1V158zm-29.259.5h28.759v-1H84.793zm-.5-117.857V158h1V40.643zM46.95 72.785v-1a1 1 0 0 0-1 1zm0 85.214V72.785h-1V158zm28.258-.5H46.45v1h28.758zm-.5-84.714V158h1V72.785zm0 0h1a1 1 0 0 0-1-1zm-27.758 0h27.758v-1H46.95zM8.604 94.215v-1a1 1 0 0 0-1 1zm0 63.785V94.215h-1V158zm28.258-.5H8.104v1h28.758zm-.5-63.285V158h1V94.215zm0 0h1a1 1 0 0 0-1-1zm-27.758 0h27.758v-1H8.604z"}))),s=(0,a.forwardRef)(o)},50317:(e,t,r)=>{r.d(t,{A:()=>u});var l=r(96540),i=r(17437),a=r(96453),n=r(78518),o=r(66537),s=r(19129),c=r(40563),d=r(67073),h=r(2445);const p=i.AH`
  &.anticon {
    font-size: unset;
    .anticon {
      line-height: unset;
      vertical-align: unset;
    }
  }
`,u=({name:e,label:t,description:r,validationErrors:u=[],renderTrigger:m=!1,rightNode:v,leftNode:f,onClick:g,hovered:b=!1,tooltipOnClick:y=()=>{},warning:x,danger:w})=>{const{gridUnit:z,colors:C}=(0,a.DP)(),F=(0,l.useRef)(!1),k=(0,l.useMemo)((()=>(u.length||(F.current=!0),F.current?u.length?C.error.base:"unset":C.warning.base)),[C.error.base,C.warning.base,u.length]);return t?(0,h.FD)("div",{className:"ControlHeader","data-test":`${e}-header`,children:[(0,h.Y)("div",{className:"pull-left",children:(0,h.FD)(c.lR,{css:e=>i.AH`
            margin-bottom: ${.5*e.gridUnit}px;
            position: relative;
          `,children:[f&&(0,h.Y)("span",{children:f}),(0,h.Y)("span",{role:"button",tabIndex:0,onClick:g,style:{cursor:g?"pointer":""},children:t})," ",x&&(0,h.FD)("span",{children:[(0,h.Y)(s.m_,{id:"error-tooltip",placement:"top",title:x,children:(0,h.Y)(d.F.WarningOutlined,{iconColor:C.warning.base,css:i.AH`
                    vertical-align: baseline;
                  `,iconSize:"s"})})," "]}),w&&(0,h.FD)("span",{children:[(0,h.Y)(s.m_,{id:"error-tooltip",placement:"top",title:w,children:(0,h.Y)(d.F.ExclamationCircleOutlined,{iconColor:C.error.base,iconSize:"s"})})," "]}),(null==u?void 0:u.length)>0&&(0,h.FD)("span",{"data-test":"error-tooltip",children:[(0,h.Y)(s.m_,{id:"error-tooltip",placement:"top",title:null==u?void 0:u.join(" "),children:(0,h.Y)(d.F.ExclamationCircleOutlined,{css:i.AH`
                    ${p};
                    color: ${k};
                  `})})," "]}),b?(0,h.FD)("span",{css:()=>i.AH`
          position: absolute;
          top: 50%;
          right: 0;
          padding-left: ${z}px;
          transform: translate(100%, -50%);
          white-space: nowrap;
        `,children:[r&&(0,h.FD)("span",{children:[(0,h.Y)(s.m_,{id:"description-tooltip",title:r,placement:"top",children:(0,h.Y)(d.F.InfoCircleOutlined,{css:p,onClick:y})})," "]}),m&&(0,h.FD)("span",{children:[(0,h.Y)(o.W,{label:(0,n.t)("bolt"),tooltip:(0,n.t)("Changing this control takes effect instantly"),placement:"top",icon:"bolt"})," "]})]}):null]})}),v&&(0,h.Y)("div",{className:"pull-right",children:v}),(0,h.Y)("div",{className:"clearfix"})]}):null}},50455:(e,t,r)=>{r.d(t,{p:()=>Ge});var l,i,a,n,o,s=r(96453),c=r(17437),d=r(78518),h=r(46920),p=r(96540);function u(){return u=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},u.apply(null,arguments)}const m=({title:e,titleId:t,...r},s)=>p.createElement("svg",u({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 120 150",ref:s,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,l||(l=p.createElement("path",{fill:"currentColor",fillOpacity:.25,stroke:"currentColor",d:"M100.133 19.84h.001L119.5 40.696V149.5H.5V.5h81.781z"})),i||(i=p.createElement("path",{stroke:"currentColor",d:"M82.5 0v42H120"})),a||(a=p.createElement("rect",{width:71.778,height:9.444,x:24,y:65,fill:"currentColor",fillOpacity:.5,stroke:"currentColor",strokeWidth:2,mask:"url(#filter-results_svg__path-3-inside-1_738_30486)",rx:.5})),n||(n=p.createElement("rect",{width:41.556,height:9.444,x:39.111,y:85.778,fill:"currentColor",fillOpacity:.5,stroke:"currentColor",strokeWidth:2,mask:"url(#filter-results_svg__path-4-inside-2_738_30486)",rx:.5})),o||(o=p.createElement("rect",{width:18.889,height:9.444,x:50.444,y:106.556,fill:"currentColor",fillOpacity:.5,stroke:"currentColor",strokeWidth:2,mask:"url(#filter-results_svg__path-5-inside-3_738_30486)",rx:.5}))),v=(0,p.forwardRef)(m);var f,g,b,y=r(46e3);function x(){return x=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},x.apply(null,arguments)}const w=({title:e,titleId:t,...r},l)=>p.createElement("svg",x({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 75 53",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,f||(f=p.createElement("rect",{width:71.778,height:9.444,x:.798,fill:"currentColor",fillOpacity:.5,stroke:"currentColor",rx:.5})),g||(g=p.createElement("rect",{width:41.556,height:9.444,x:15.909,y:20.777,fill:"currentColor",fillOpacity:.5,stroke:"currentColor",rx:.5})),b||(b=p.createElement("rect",{width:18.889,height:9.444,x:27.243,y:41.556,fill:"currentColor",fillOpacity:.5,stroke:"currentColor",rx:.5}))),z=(0,p.forwardRef)(w);var C,F,k;function E(){return E=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},E.apply(null,arguments)}const Y=({title:e,titleId:t,...r},l)=>p.createElement("svg",E({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 119 78",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,C||(C=p.createElement("rect",{width:86,height:62,x:16,y:1,stroke:"currentColor",strokeWidth:2,rx:3})),F||(F=p.createElement("path",{fill:"currentColor",d:"M60 32.642h20c.902 0 1.918 1.999 1.918 1.999-1.016 12.32-11.336 22-23.918 22v-24Z"})),k||(k=p.createElement("path",{fill:"currentColor",fillOpacity:.5,d:"M58 10.642c0-1.105-.899-2.01-2-1.918C43.682 9.74 34 20.06 34 32.642c0 13.255 10.745 24 24 24 12.582 0 22.902-9.682 23.918-22.001.09-1.1-.813-2-1.918-2H60a2 2 0 0 1-2-2z"}))),S=(0,p.forwardRef)(Y);var M,$,O,A,V,I;function H(){return H=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},H.apply(null,arguments)}const D=({title:e,titleId:t,...r},l)=>p.createElement("svg",H({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 119 78",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,M||(M=p.createElement("rect",{width:86,height:62,x:17,y:1,stroke:"currentColor",strokeWidth:2,rx:3})),$||($=p.createElement("rect",{width:78,height:14,x:21,y:5,stroke:"currentColor",strokeWidth:2,rx:3})),O||(O=p.createElement("rect",{width:38,height:36,x:21,y:23,stroke:"currentColor",strokeWidth:2,rx:3})),A||(A=p.createElement("rect",{width:36,height:22,x:63,y:37,stroke:"currentColor",strokeWidth:2,rx:3})),V||(V=p.createElement("rect",{width:36,height:10,x:63,y:23,stroke:"currentColor",strokeWidth:2,rx:3})),I||(I=p.createElement("path",{fill:"currentColor",fillOpacity:.25,fillRule:"evenodd",stroke:"currentColor",d:"M16 55.29C6.074 57.7 0 60.94 0 64.5 0 71.956 26.64 78 59.5 78S119 71.956 119 64.5c0-3.44-5.668-6.578-15-8.962V60a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4z",clipRule:"evenodd"}))),N=(0,p.forwardRef)(D);var _,R;function U(){return U=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},U.apply(null,arguments)}const j=({title:e,titleId:t,...r},l)=>p.createElement("svg",U({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 119 76",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,_||(_=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M83.195 1.366 103 24v38a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4V24L35.805 1.366A4 4 0 0 1 38.815 0h41.37a4 4 0 0 1 3.01 1.366M101 26v36a2 2 0 0 1-2 2H20a2 2 0 0 1-2-2V26h17.25A4.75 4.75 0 0 1 40 30.75a6.75 6.75 0 0 0 6.75 6.75h25.5A6.75 6.75 0 0 0 79 30.75 4.75 4.75 0 0 1 83.75 26zm-.658-2L81.69 2.683A2 2 0 0 0 80.185 2h-41.37a2 2 0 0 0-1.505.683L18.657 24H35.25A6.75 6.75 0 0 1 42 30.75a4.75 4.75 0 0 0 4.75 4.75h25.5A4.75 4.75 0 0 0 77 30.75 6.75 6.75 0 0 1 83.75 24z",clipRule:"evenodd"})),R||(R=p.createElement("path",{fill:"currentColor",fillOpacity:.25,stroke:"currentColor",d:"M16 53.29C6.074 55.7 0 58.94 0 62.5 0 69.956 26.64 76 59.5 76S119 69.956 119 62.5c0-3.56-6.074-6.799-16-9.21V62a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4z"}))),T=(0,p.forwardRef)(j);var L,P,B,q,W,K,Z,G,J,Q;function X(){return X=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},X.apply(null,arguments)}const ee=({title:e,titleId:t,...r},l)=>p.createElement("svg",X({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 119 78",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,L||(L=p.createElement("path",{stroke:"currentColor",strokeWidth:2,d:"M37 4a3 3 0 0 1 3-3h30.343a3 3 0 0 1 2.121.879l9.657 9.657a3 3 0 0 1 .879 2.12V60a3 3 0 0 1-3 3H40a3 3 0 0 1-3-3z"})),P||(P=p.createElement("path",{stroke:"currentColor",strokeWidth:2,d:"M71 .5V9a4 4 0 0 0 4 4h8.5M71 27v18c0 1.074-.897 2.316-2.962 3.348C66.033 49.351 63.192 50 60 50s-6.033-.65-8.038-1.652C49.897 47.316 49 46.074 49 45V27c0-1.074.897-2.316 2.962-3.348C53.967 22.649 56.808 22 60 22s6.033.65 8.038 1.652C70.103 24.684 71 25.926 71 27Z"})),B||(B=p.createElement("mask",{id:"empty-queries_svg__a",fill:"#fff"},p.createElement("path",{fillRule:"evenodd",d:"M48 39c0 3.314 5.373 6 12 6s12-2.686 12-6h-2.087c0 .536-.475 1.51-2.393 2.47C65.703 42.378 63.047 43 60 43s-5.703-.622-7.52-1.53c-1.918-.96-2.393-1.934-2.393-2.47z",clipRule:"evenodd"}))),q||(q=p.createElement("path",{fill:"#000",fillRule:"evenodd",d:"M48 39c0 3.314 5.373 6 12 6s12-2.686 12-6h-2.087c0 .536-.475 1.51-2.393 2.47C65.703 42.378 63.047 43 60 43s-5.703-.622-7.52-1.53c-1.918-.96-2.393-1.934-2.393-2.47z",clipRule:"evenodd"})),W||(W=p.createElement("path",{fill:"currentColor",d:"M48 39v-2h-2v2zm24 0h2v-2h-2zm-2.087 0v-2h-2v2zM52.48 41.47l-.894 1.788zM50.087 39h2v-2h-2zM46 39c0 2.822 2.236 4.84 4.62 6.032C53.124 46.283 56.443 47 60 47v-4c-3.07 0-5.751-.626-7.59-1.546C50.45 40.474 50 39.49 50 39zm14 8c3.557 0 6.876-.717 9.38-1.968C71.764 43.839 74 41.822 74 39h-4c0 .491-.45 1.474-2.41 2.454C65.752 42.374 63.07 43 60 43zm12-10h-2.087v4H72zm-3.586 6.258c2.158-1.078 3.499-2.575 3.499-4.258h-4c0-.312.126-.371-.014-.204-.135.162-.487.491-1.273.885zM60 45c3.29 0 6.265-.667 8.414-1.742l-1.788-3.577C65.14 40.423 62.804 41 60 41zm-8.414-1.742C53.736 44.333 56.709 45 60 45v-4c-2.804 0-5.14-.577-6.626-1.32zM48.087 39c0 1.683 1.341 3.18 3.499 4.258l1.788-3.577c-.787-.394-1.138-.723-1.273-.885-.14-.167-.014-.108-.014.204zm2-2H48v4h2.087z",mask:"url(#empty-queries_svg__a)"})),K||(K=p.createElement("mask",{id:"empty-queries_svg__b",fill:"#fff"},p.createElement("path",{fillRule:"evenodd",d:"M48 33c0 3.314 5.373 6 12 6s12-2.686 12-6h-2.087c0 .536-.475 1.51-2.393 2.47C65.703 36.378 63.047 37 60 37s-5.703-.622-7.52-1.53c-1.918-.96-2.393-1.934-2.393-2.47z",clipRule:"evenodd"}))),Z||(Z=p.createElement("path",{fill:"#000",fillRule:"evenodd",d:"M48 33c0 3.314 5.373 6 12 6s12-2.686 12-6h-2.087c0 .536-.475 1.51-2.393 2.47C65.703 36.378 63.047 37 60 37s-5.703-.622-7.52-1.53c-1.918-.96-2.393-1.934-2.393-2.47z",clipRule:"evenodd"})),G||(G=p.createElement("path",{fill:"currentColor",d:"M48 33v-2h-2v2zm24 0h2v-2h-2zm-2.087 0v-2h-2v2zM52.48 35.47l-.894 1.788zM50.087 33h2v-2h-2zM46 33c0 2.822 2.236 4.84 4.62 6.032C53.124 40.283 56.443 41 60 41v-4c-3.07 0-5.751-.626-7.59-1.546C50.45 34.474 50 33.49 50 33zm14 8c3.557 0 6.876-.717 9.38-1.968C71.764 37.839 74 35.822 74 33h-4c0 .491-.45 1.474-2.41 2.454C65.752 36.374 63.07 37 60 37zm12-10h-2.087v4H72zm-3.586 6.258c2.158-1.078 3.499-2.575 3.499-4.258h-4c0-.312.126-.371-.014-.204-.135.162-.487.491-1.273.885zM60 39c3.29 0 6.265-.667 8.414-1.742l-1.788-3.577C65.14 34.423 62.804 35 60 35zm-8.414-1.742C53.736 38.333 56.709 39 60 39v-4c-2.804 0-5.14-.577-6.626-1.32zM48.087 33c0 1.683 1.341 3.18 3.499 4.258l1.788-3.577c-.787-.394-1.138-.723-1.273-.885-.14-.167-.014-.108-.014.204zm2-2H48v4h2.087z",mask:"url(#empty-queries_svg__b)"})),J||(J=p.createElement("path",{stroke:"currentColor",strokeWidth:2,d:"M71 27c0 1.074-.897 2.316-2.962 3.348C66.033 31.351 63.192 32 60 32s-6.033-.65-8.038-1.652C49.897 29.316 49 28.074 49 27s.897-2.316 2.962-3.348C53.967 22.649 56.808 22 60 22s6.033.65 8.038 1.652C70.103 24.684 71 25.926 71 27Z"})),Q||(Q=p.createElement("path",{fill:"currentColor",fillOpacity:.25,fillRule:"evenodd",stroke:"currentColor",d:"M36 51.134C14.826 53.278 0 58.232 0 64c0 7.732 26.64 14 59.5 14S119 71.732 119 64c0-5.677-14.36-10.565-35-12.762V60a4 4 0 0 1-4 4H40a4 4 0 0 1-4-4z",clipRule:"evenodd"}))),te=(0,p.forwardRef)(ee);var re,le;function ie(){return ie=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},ie.apply(null,arguments)}const ae=({title:e,titleId:t,...r},l)=>p.createElement("svg",ie({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 119 78",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,re||(re=p.createElement("path",{stroke:"currentColor",strokeWidth:2,d:"M59.212 1.559c.245-.745 1.33-.745 1.576 0l6.774 20.573a2.825 2.825 0 0 0 2.687 1.933h21.92a.8.8 0 0 1 .492 1.45L74.927 38.23a2.79 2.79 0 0 0-1.031 3.14l6.774 20.574c.229.696-.594 1.382-1.28.89L61.658 50.12a2.85 2.85 0 0 0-3.314 0L40.61 62.835c-.685.491-1.508-.195-1.279-.89l6.774-20.574a2.79 2.79 0 0 0-1.03-3.142L27.338 25.515a.8.8 0 0 1 .492-1.449h21.92a2.825 2.825 0 0 0 2.687-1.933z"})),le||(le=p.createElement("path",{fill:"currentColor",fillOpacity:.25,fillRule:"evenodd",stroke:"currentColor",d:"M41.678 51.616C17.524 53.334 0 58.453 0 64.5 0 71.956 26.64 78 59.5 78S119 71.956 119 64.5c0-5.961-17.03-11.02-40.653-12.809l3.272 9.94c.547 1.662-1.38 3.043-2.811 2.017L61.176 51.005a267 267 0 0 0-2.346-.004L41.192 63.648c-1.432 1.026-3.358-.355-2.811-2.016z",clipRule:"evenodd"}))),ne=(0,p.forwardRef)(ae);var oe;function se(){return se=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},se.apply(null,arguments)}const ce=({title:e,titleId:t,...r},l)=>p.createElement("svg",se({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 118 150",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,oe||(oe=p.createElement("path",{fill:"currentColor",fillOpacity:.5,stroke:"CurrentColor",d:"M12.121 11.554h-.5v35.821h94.75V11.554h-94.25Zm93.75 81.357h.5V57.089h-94.75v35.822h94.25Zm0 45.535h.5v-35.821h-94.75v35.821h94.25ZM5.425.5h107.143a4.85 4.85 0 0 1 4.857 4.857v139.286a4.85 4.85 0 0 1-4.857 4.857H5.425a4.85 4.85 0 0 1-4.857-4.857V5.357A4.85 4.85 0 0 1 5.425.5ZM26.49 33.846a6.196 6.196 0 1 1 8.762-8.763 6.196 6.196 0 0 1-8.762 8.763Zm0 45.536a6.196 6.196 0 1 1 8.762-8.763 6.196 6.196 0 0 1-8.762 8.763Zm0 45.535a6.196 6.196 0 1 1 8.761-8.762 6.196 6.196 0 0 1-8.761 8.762Z"}))),de=(0,p.forwardRef)(ce);var he,pe;function ue(){return ue=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},ue.apply(null,arguments)}const me=({title:e,titleId:t,...r},l)=>p.createElement("svg",ue({xmlns:"http://www.w3.org/2000/svg",width:64,height:80,fill:"none",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,he||(he=p.createElement("path",{fill:"currentColor",fillOpacity:.5,stroke:"currentColor",d:"M53.233 10.74 63.5 21.796V79.5H.5V.5h43.281z"})),pe||(pe=p.createElement("path",{stroke:"currentColor",d:"M44 0v22.4h20"}))),ve=(0,p.forwardRef)(me);var fe,ge;function be(){return be=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},be.apply(null,arguments)}const ye=({title:e,titleId:t,...r},l)=>p.createElement("svg",be({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 152 152",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,fe||(fe=p.createElement("path",{fill:"currentColor",d:"M44.5 1a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM97.5 1a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM150.5 1a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM44.5 54a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V55a1 1 0 0 1 1-1zM97.5 54a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V55a1 1 0 0 1 1-1zM150.5 54a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V55a1 1 0 0 1 1-1zM44.5 106a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1v-43a1 1 0 0 1 1-1zM97.5 106a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1v-43a1 1 0 0 1 1-1zM150.5 106a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1v-43a1 1 0 0 1 1-1z"})),ge||(ge=p.createElement("path",{stroke:"currentColor",d:"M44.5 1a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM97.5 1a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM150.5 1a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM44.5 54a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V55a1 1 0 0 1 1-1zM97.5 54a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V55a1 1 0 0 1 1-1zM150.5 54a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1V55a1 1 0 0 1 1-1zM44.5 106a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1v-43a1 1 0 0 1 1-1zM97.5 106a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1v-43a1 1 0 0 1 1-1zM150.5 106a1 1 0 0 1 1 1v43a1 1 0 0 1-1 1h-43a1 1 0 0 1-1-1v-43a1 1 0 0 1 1-1z"}))),xe=(0,p.forwardRef)(ye);var we,ze;function Ce(){return Ce=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},Ce.apply(null,arguments)}const Fe=({title:e,titleId:t,...r},l)=>p.createElement("svg",Ce({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 196 152",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,we||(we=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M193.652 1.5a.5.5 0 0 0-.5-.5H52.348v29.348h140.804a.5.5 0 0 0 .5-.5zm-152.174 0a.5.5 0 0 0-.5-.5H1.261v29.348h39.717a.5.5 0 0 0 .5-.5zm152.174 120.652a.5.5 0 0 0-.5-.5h-39.717V151h39.717a.5.5 0 0 0 .5-.5zM40.978 81.435a.5.5 0 0 1 .5.5v28.348a.5.5 0 0 1-.5.5H1.261V81.435zm75.5.5a.5.5 0 0 0-.5-.5h-63.63v29.348h63.63a.5.5 0 0 0 .5-.5zM193.761 81a.5.5 0 0 1 .5.5v29a.5.5 0 0 1-.5.5h-66.5V81zm-51.696 40.652a.5.5 0 0 1 .5.5V150.5a.5.5 0 0 1-.5.5H1.261v-29.348zm52.674-79.935a.5.5 0 0 0-.5-.5H1.261v29.348h192.978a.5.5 0 0 0 .5-.5z",clipRule:"evenodd"})),ze||(ze=p.createElement("path",{fill:"currentColor",d:"M193.152 1V.5zM52.348 1V.5h-.5V1zm0 29.348h-.5v.5h.5zm140.804 0v.5zM40.978 1v.5zM1.261 1V.5h-.5V1zm0 29.348h-.5v.5h.5zm39.717 0v.5zm112.457 91.304v-.5h-.5v.5zm0 29.348h-.5v.5h.5zM1.261 110.783h-.5v.5h.5zm0-29.348v-.5h-.5v.5zm51.087 0v-.5h-.5v.5zm0 29.348h-.5v.5h.5zm74.913.217h-.5v.5h.5zm0-30v-.5h-.5v.5zm14.804 40.652v.5zm0 29.348v.5zM1.261 151h-.5v.5h.5zm0-29.348v-.5h-.5v.5zm192.978-80.435v.5zm-192.978 0v-.5h-.5v.5zm0 29.348h-.5v.5h.5zm192.978 0v.5zM193.152 1.5h1a1 1 0 0 0-1-1zm-140.804 0h140.804v-1H52.348zm.5 28.848V1h-1v29.348zm140.304-.5H52.348v1h140.804zm0 0v1a1 1 0 0 0 1-1zm0-28.348v28.348h1V1.5zm-152.174 0h1a1 1 0 0 0-1-1zm-39.717 0h39.717v-1H1.261zm.5 28.848V1h-1v29.348zm39.217-.5H1.261v1h39.717zm0 0v1a1 1 0 0 0 1-1zm0-28.348v28.348h1V1.5zm152.174 120.652h1a1 1 0 0 0-1-1zm-39.717 0h39.717v-1h-39.717zm.5 28.848v-29.348h-1V151zm39.217-.5h-39.717v1h39.717zm0 0v1a1 1 0 0 0 1-1zm0-28.348V150.5h1v-28.348zM41.978 81.935a1 1 0 0 0-1-1v1zm0 28.348V81.935h-1v28.348zm-1 1a1 1 0 0 0 1-1h-1zm-39.717 0h39.717v-1H1.261zm-.5-29.848v29.348h1V81.435zm40.217-.5H1.261v1h39.717zm75 1h1a1 1 0 0 0-1-1zm-63.63 0h63.63v-1h-63.63zm.5 28.848V81.435h-1v29.348zm63.13-.5h-63.63v1h63.63zm0 0v1a1 1 0 0 0 1-1zm0-28.348v28.348h1V81.935zm78.783-.435a1 1 0 0 0-1-1v1zm0 29v-29h-1v29zm-1 1a1 1 0 0 0 1-1h-1zm-66.5 0h66.5v-1h-66.5zm-.5-30.5v30h1V81zm67-.5h-66.5v1h66.5zm-50.696 41.652a1 1 0 0 0-1-1v1zm0 28.348v-28.348h-1V150.5zm-1 1a1 1 0 0 0 1-1h-1zm-140.804 0h140.804v-1H1.261zm-.5-29.848V151h1v-29.348zm141.304-.5H1.261v1h140.804zm52.174-79.435h1a1 1 0 0 0-1-1zm-192.978 0h192.978v-1H1.261zm.5 28.848V41.217h-1v29.348zm192.478-.5H1.261v1h192.978zm0 0v1a1 1 0 0 0 1-1zm0-28.348v28.348h1V41.717z"}))),ke=(0,p.forwardRef)(Fe);var Ee;function Ye(){return Ye=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},Ye.apply(null,arguments)}const Se=({title:e,titleId:t,...r},l)=>p.createElement("svg",Ye({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 300 146",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,Ee||(Ee=p.createElement("path",{fill:"currentColor",d:"M17 21a4 4 0 0 1 4-4h104a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4zM17 45a4 4 0 0 1 4-4h202a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4zM21 65a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h151a4 4 0 0 0 4-4v-8a4 4 0 0 0-4-4zM17 93a4 4 0 0 1 4-4h265a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4zM21 113a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h52a4 4 0 0 0 4-4v-8a4 4 0 0 0-4-4z"}))),Me=(0,p.forwardRef)(Se);var $e,Oe;function Ae(){return Ae=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},Ae.apply(null,arguments)}const Ve=({title:e,titleId:t,...r},l)=>p.createElement("svg",Ae({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 81 82",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,$e||($e=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M76.5 1h-72a4 4 0 0 0-4 4v72a4 4 0 0 0 4 4h72a4 4 0 0 0 4-4V5a4 4 0 0 0-4-4m-40 72h-28V57h28zm0-24h-28V33h28zm36 24h-28V57h28zm0-24h-28V33h28zm0-24h-64V9h64z",clipRule:"evenodd"})),Oe||(Oe=p.createElement("path",{fill:"currentColor",d:"M36.5 73v.5h.5V73zm-28 0H8v.5h.5zm0-16v-.5H8v.5zm28 0h.5v-.5h-.5zm0-8v.5h.5V49zm-28 0H8v.5h.5zm0-16v-.5H8v.5zm28 0h.5v-.5h-.5zm36 40v.5h.5V73zm-28 0H44v.5h.5zm0-16v-.5H44v.5zm28 0h.5v-.5h-.5zm0-8v.5h.5V49zm-28 0H44v.5h.5zm0-16v-.5H44v.5zm28 0h.5v-.5h-.5zm0-8v.5h.5V25zm-64 0H8v.5h.5zm0-16v-.5H8V9zm64 0h.5v-.5h-.5zm4-8.5h-72v1h72zm-72 0A4.5 4.5 0 0 0 0 5h1a3.5 3.5 0 0 1 3.5-3.5zM0 5v72h1V5zm0 72a4.5 4.5 0 0 0 4.5 4.5v-1A3.5 3.5 0 0 1 1 77zm4.5 4.5h72v-1h-72zm72 0A4.5 4.5 0 0 0 81 77h-1a3.5 3.5 0 0 1-3.5 3.5zM81 77V5h-1v72zm0-72A4.5 4.5 0 0 0 76.5.5v1A3.5 3.5 0 0 1 80 5zM36.5 72.5h-28v1h28zM9 73V57H8v16zm-.5-15.5h28v-1h-28zM36 57v16h1V57zm.5-8.5h-28v1h28zM9 49V33H8v16zm-.5-15.5h28v-1h-28zM36 33v16h1V33zm36.5 39.5h-28v1h28zM45 73V57h-1v16zm-.5-15.5h28v-1h-28zM72 57v16h1V57zm.5-8.5h-28v1h28zM45 49V33h-1v16zm-.5-15.5h28v-1h-28zM72 33v16h1V33zm.5-8.5h-64v1h64zM9 25V9H8v16zM8.5 9.5h64v-1h-64zM72 9v16h1V9z"}))),Ie=(0,p.forwardRef)(Ve);var He,De;function Ne(){return Ne=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var l in r)({}).hasOwnProperty.call(r,l)&&(e[l]=r[l])}return e},Ne.apply(null,arguments)}const _e=({title:e,titleId:t,...r},l)=>p.createElement("svg",Ne({xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 119 76",ref:l,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,He||(He=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M83.195 1.366 103 24v38a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4V24L35.805 1.366A4 4 0 0 1 38.815 0h41.37a4 4 0 0 1 3.01 1.366M101 26v36a2 2 0 0 1-2 2H20a2 2 0 0 1-2-2V26h17.25A4.75 4.75 0 0 1 40 30.75a6.75 6.75 0 0 0 6.75 6.75h25.5A6.75 6.75 0 0 0 79 30.75 4.75 4.75 0 0 1 83.75 26zm-.658-2L81.69 2.683A2 2 0 0 0 80.185 2h-41.37a2 2 0 0 0-1.505.683L18.657 24H35.25A6.75 6.75 0 0 1 42 30.75a4.75 4.75 0 0 0 4.75 4.75h25.5A4.75 4.75 0 0 0 77 30.75 6.75 6.75 0 0 1 83.75 24z",clipRule:"evenodd"})),De||(De=p.createElement("path",{fill:"currentColor",fillOpacity:.25,stroke:"currentColor",d:"M16 53.29C6.074 55.7 0 58.94 0 62.5 0 69.956 26.64 76 59.5 76S119 69.956 119 62.5c0-3.56-6.074-6.799-16-9.21V62a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4z"}))),Re=(0,p.forwardRef)(_e);var Ue=r(641),je=r(2445);const Te={"chart.svg":(0,je.Y)(y.A,{}),"document.svg":(0,je.Y)(ve,{}),"empty-charts.svg":(0,je.Y)(S,{}),"empty-dashboard.svg":(0,je.Y)(N,{}),"empty-dataset.svg":(0,je.Y)(xe,{}),"empty-queries.svg":(0,je.Y)(te,{}),"empty-query.svg":(0,je.Y)(Me,{}),"empty-table.svg":(0,je.Y)(Ie,{}),"empty.svg":(0,je.Y)(Re,{}),"empty_sql_chart.svg":(0,je.Y)(ke,{}),"filter-results.svg":(0,je.Y)(v,{}),"filter.svg":(0,je.Y)(z,{}),"star-circle.svg":(0,je.Y)(ne,{}),"union.svg":(0,je.Y)(T,{}),"vector.svg":(0,je.Y)(de,{})},Le=s.I4.div`
  ${({theme:e})=>c.AH`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    color: ${e.colors.grayscale.light2};
    align-items: center;
    justify-content: center;
    padding: ${4*e.gridUnit}px;
    text-align: center;

    & .antd5-empty-image svg {
      width: auto;
    }

    & a,
    & span[role='button'] {
      color: inherit;
      text-decoration: underline;
      &:hover {
        color: ${e.colors.grayscale.base};
      }
    }
  `}
`,Pe=s.I4.p`
  ${({theme:e,size:t})=>c.AH`
    font-size: ${"large"===t?e.typography.sizes.l:e.typography.sizes.m}px;
    color: ${e.colors.grayscale.light1};
    margin-top: ${"large"===t?4*e.gridUnit:2*e.gridUnit}px;
    font-weight: ${e.typography.weights.bold};
  `}
`,Be=s.I4.p`
  ${({theme:e,size:t})=>c.AH`
    font-size: ${"large"===t?e.typography.sizes.m:e.typography.sizes.s}px;
    color: ${e.colors.grayscale.light1};
    margin-top: ${2*e.gridUnit}px;
  `}
`,qe=(0,s.I4)(h.A)`
  ${({theme:e})=>c.AH`
    margin-top: ${4*e.gridUnit}px;
    z-index: 1;
  `}
`,We=e=>{switch(e){case"small":return{height:"50px"};case"medium":default:return{height:"80px"};case"large":return{height:"150px"}}},Ke=({image:e,size:t})=>{if(!e)return null;const r="string"==typeof e?Te[e]:e;return(0,je.Y)("div",{role:"img","aria-label":"empty",children:(0,je.Y)(Ue.S,{description:!1,image:r,imageStyle:We(t)})})},Ze=e=>{e.preventDefault(),e.stopPropagation()},Ge=({title:e=(0,d.t)("No results"),description:t=(0,d.t)("There is currently no information to display."),image:r="empty.svg",buttonText:l,buttonAction:i,size:a="medium",children:n})=>(0,je.FD)(Le,{children:[r&&(0,je.Y)(Ke,{image:r,size:a}),(0,je.FD)("div",{css:e=>c.AH`
        max-width: ${"large"===a?150*e.gridUnit:100*e.gridUnit}px;
      `,children:[e&&(0,je.Y)(Pe,{size:a,children:e}),t&&(0,je.Y)(Be,{size:a,className:"ant-empty-description",children:t}),l&&i&&(0,je.Y)(qe,{buttonStyle:"primary",onClick:i,onMouseDown:Ze,children:l}),n]})]})},58132:(e,t,r)=>{r.d(t,{A:()=>s});var l=r(96453),i=r(78518),a=r(67073),n=r(19129),o=r(2445);const s=function({certifiedBy:e,details:t,size:r="l"}){const s=(0,l.DP)();return(0,o.Y)(n.m_,{id:"certified-details-tooltip",title:(0,o.FD)(o.FK,{children:[e&&(0,o.Y)("div",{children:(0,o.Y)("strong",{children:(0,i.t)("Certified by %s",e)})}),(0,o.Y)("div",{children:t})]}),children:(0,o.Y)(a.F.Certified,{iconColor:s.colors.primary.base,iconSize:r})})}},73312:(e,t,r)=>{r.d(t,{A:()=>R});var l=r(90179),i=r.n(l),a=r(96540),n=r(90868),o=r(40563),s=r(75086),c=r.n(s),d=r(46920),h=r(15595),p=r(58561),u=r.n(p),m=r(96453),v=r(78518),f=r(76968),g=r(51436),b=r(35742),y=r(62952),x=r(27366),w=r(17437),z=r(85861),C=r(24976),F=r(76125),k=r(2445);const E=({colorScheme:e,hasCustomLabelsColor:t=!1,hovered:r=!1,onChange:l=()=>{}})=>{const[i,n]=(0,a.useState)([]),[o,s]=(0,a.useState)({});return(0,a.useEffect)((()=>{const e=(0,f.A)();n(e.keys().map((e=>[e,e]))),s(e.getMap())}),[]),(0,k.Y)(F.A,{description:(0,v.t)("Any color palette selected here will override the colors applied to this dashboard's individual charts"),name:"color_scheme",onChange:l,value:null!=e?e:"",choices:i,clearable:!0,hovered:r,schemes:o,hasCustomLabelsColor:t})};var Y=r(888),S=r(5261),M=r(97567),$=r(3932),O=r(55556),A=r(25106),V=r(61225),I=r(72173),H=r(35839);const D=(0,m.I4)(o.eI)`
  margin-bottom: 0;
`,N=(0,m.I4)(C.iN)`
  border-radius: ${({theme:e})=>e.borderRadius}px;
  border: 1px solid ${({theme:e})=>e.colors.secondary.light2};
`;var _={name:"1blj7km",styles:"margin-top:1em"};const R=(0,S.Ay)((({addSuccessToast:e,addDangerToast:t,colorScheme:r,dashboardId:l,dashboardInfo:s,dashboardTitle:p,onHide:m=()=>{},onlyApply:F=!1,onSubmit:S=()=>{},show:R=!1})=>{const U=(0,V.wA)(),[j]=h.Wq.useForm(),[T,L]=(0,a.useState)(!1),[P,B]=(0,a.useState)(!1),[q,W]=(0,a.useState)(r),[K,Z]=(0,a.useState)(""),[G,J]=(0,a.useState)(),[Q,X]=(0,a.useState)([]),[ee,te]=(0,a.useState)([]),re=F?(0,v.t)("Apply"):(0,v.t)("Save"),[le,ie]=(0,a.useState)([]),ae=(0,f.A)(),ne=(0,a.useRef)({}),oe=(0,a.useMemo)((()=>le.map((e=>({value:e.id,label:e.name})))),[le.length]),se=async e=>{const{error:t,statusText:r,message:l}=await(0,g.h4)(e);let i=t||r||(0,v.t)("An error has occurred");"object"==typeof l&&"json_metadata"in l?i=l.json_metadata:"string"==typeof l&&(i=l,"Forbidden"===l&&(i=(0,v.t)("You do not have permission to edit this dashboard"))),z.Ay.error({title:(0,v.t)("Error"),content:i,okButtonProps:{danger:!0,className:"btn-danger"}})},ce=(0,a.useCallback)(((e="owners",t="",r,l)=>{const i=u().encode({filter:t,page:r,page_size:l});return b.A.get({endpoint:`/api/v1/dashboard/related/${e}?q=${i}`}).then((e=>({data:e.json.result.filter((e=>void 0===e.extra.active||e.extra.active)).map((e=>({value:e.value,label:e.text}))),totalCount:e.json.count})))}),[]),de=(0,a.useCallback)((e=>{const{id:t,dashboard_title:r,slug:l,certified_by:a,certification_details:n,owners:o,roles:s,metadata:d,is_managed_externally:h}=e,p={id:t,title:r,slug:l||"",certifiedBy:a||"",certificationDetails:n||"",isManagedExternally:h||!1,metadata:d};j.setFieldsValue(p),J(p),X(o),te(s),W(d.color_scheme);const u=i()(d,["positions","shared_label_colors","map_label_colors","color_scheme_domain"]);Z(u?c()(u):""),ne.current=d}),[j]),he=(0,a.useCallback)((()=>{L(!0),b.A.get({endpoint:`/api/v1/dashboard/${l}`}).then((e=>{var t;const r=e.json.result,l=null!=(t=r.json_metadata)&&t.length?JSON.parse(r.json_metadata):{};de({...r,metadata:l}),L(!1)}),se)}),[l,de]),pe=()=>{try{return null!=K&&K.length?JSON.parse(K):{}}catch(e){return{}}},ue=e=>{const t=(0,y.A)(e).map((e=>({id:e.value,full_name:e.label})));X(t)},me=e=>{const t=(0,y.A)(e).map((e=>({id:e.value,name:e.label})));te(t)},ve=()=>(Q||[]).map((e=>({value:e.id,label:(0,A.A)(e)}))),fe=()=>m(),ge=(e="",{updateMetadata:t=!0}={})=>{const r=ae.keys(),l=pe();if(e&&!r.includes(e))throw z.Ay.error({title:(0,v.t)("Error"),content:(0,v.t)("A valid color scheme is required"),okButtonProps:{danger:!0,className:"btn-danger"}}),m(),new Error("A valid color scheme is required");l.color_scheme=e,l.label_colors=l.label_colors||{},W(e),U((0,I.r7)(e)),t&&Z(c()(l))};return(0,a.useEffect)((()=>{R&&(s?de(s):he()),C.iN.preload()}),[s,he,de,R]),(0,a.useEffect)((()=>{p&&G&&G.title!==p&&j.setFieldsValue({...G,title:p})}),[G,p,j]),(0,a.useEffect)((()=>{if((0,x.G7)(x.TO.TaggingSystem))try{(0,M.un)({objectType:M.iQ.DASHBOARD,objectId:l,includeTypes:!1},(e=>ie(e)),(e=>{t(`Error fetching tags: ${e.text}`)}))}catch(e){se(e)}}),[l]),(0,k.Y)(z.Ay,{show:R,onHide:fe,title:(0,v.t)("Dashboard properties"),footer:(0,k.FD)(k.FK,{children:[(0,k.Y)(d.A,{htmlType:"button",buttonSize:"small",onClick:fe,"data-test":"properties-modal-cancel-button",cta:!0,children:(0,v.t)("Cancel")}),(0,k.Y)(d.A,{"data-test":"properties-modal-apply-button",onClick:j.submit,buttonSize:"small",buttonStyle:"primary",className:"m-r-5",cta:!0,disabled:null==G?void 0:G.isManagedExternally,tooltip:null!=G&&G.isManagedExternally?(0,v.t)("This dashboard is managed externally, and can't be edited in Superset"):"",children:re})]}),responsive:!0,children:(0,k.FD)(h.Wq,{form:j,onFinish:()=>{var i,a,n,o;const{title:s,slug:d,certifiedBy:h,certificationDetails:p}=j.getFieldsValue();let u,f=K;try{if(!f.startsWith("{")||!f.endsWith("}"))throw new Error;u=JSON.parse(f)}catch(e){return void t((0,v.t)("JSON metadata is invalid!"))}const g=(0,O.Z6)(null==(i=u)?void 0:i.color_namespace),y=(null==(a=u)?void 0:a.color_scheme)||q,w=y!==ne.current.color_scheme,z=!(0,H.r$)(ne.current.label_colors||{},(null==(n=u)?void 0:n.label_colors)||{}),C=Object.keys((null==(o=u)?void 0:o.label_colors)||{}),k=Object.keys(ne.current.label_colors||{}),E=C.length>0?C:k,Y=!!(z&&E.length>0)&&E,M=pe().label_colors||{},$={...ne.current,label_colors:M,color_scheme:y};ne.current=$,(0,O.D2)($,w||Y),U((0,I.Qn)({...$,map_label_colors:(0,O.xV)(M)})),ge(y,{updateMetadata:!1}),f=c()(u);const A={},V={};(0,x.G7)(x.TO.DashboardRbac)&&(A.roles=ee,V.roles=(ee||[]).map((e=>e.id))),(0,x.G7)(x.TO.TaggingSystem)&&(V.tags=le.map((e=>e.id)));const D={id:l,title:s,slug:d,jsonMetadata:f,owners:Q,colorScheme:r,colorNamespace:g,certifiedBy:h,certificationDetails:p,...A};F?(S(D),m(),e((0,v.t)("Dashboard properties updated"))):b.A.put({endpoint:`/api/v1/dashboard/${l}`,headers:{"Content-Type":"application/json"},body:JSON.stringify({dashboard_title:s,slug:d||null,json_metadata:f||null,owners:(Q||[]).map((e=>e.id)),certified_by:h||null,certification_details:h&&p?p:null,...V})}).then((()=>{S(D),m(),e((0,v.t)("The dashboard has been saved"))}),se)},"data-test":"dashboard-edit-properties-form",layout:"vertical",initialValues:G,children:[(0,k.Y)(h.fI,{children:(0,k.Y)(h.fv,{xs:24,md:24,children:(0,k.Y)("h3",{children:(0,v.t)("Basic information")})})}),(0,k.FD)(h.fI,{gutter:16,children:[(0,k.Y)(h.fv,{xs:24,md:12,children:(0,k.Y)(o.eI,{label:(0,v.t)("Name"),name:"title",children:(0,k.Y)(n.pd,{"data-test":"dashboard-title-input",type:"text",disabled:T})})}),(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)(D,{label:(0,v.t)("URL slug"),name:"slug",children:(0,k.Y)(n.pd,{type:"text",disabled:T})}),(0,k.Y)("p",{className:"help-block",children:(0,v.t)("A readable URL for your dashboard")})]})]}),(0,x.G7)(x.TO.DashboardRbac)?(()=>{const e=pe(),t=!!Object.keys((null==e?void 0:e.label_colors)||{}).length;return(0,k.FD)(k.FK,{children:[(0,k.Y)(h.fI,{children:(0,k.Y)(h.fv,{xs:24,md:24,children:(0,k.Y)("h3",{style:{marginTop:"1em"},children:(0,v.t)("Access")})})}),(0,k.FD)(h.fI,{gutter:16,children:[(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)(D,{label:(0,v.t)("Owners"),children:(0,k.Y)(h.DW,{allowClear:!0,allowNewOptions:!0,ariaLabel:(0,v.t)("Owners"),disabled:T,mode:"multiple",onChange:ue,options:(e,t,r)=>ce("owners",e,t,r),value:ve()})}),(0,k.Y)("p",{className:"help-block",children:(0,v.t)("Owners is a list of users who can alter the dashboard. Searchable by name or username.")})]}),(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)(D,{label:(0,v.t)("Roles"),children:(0,k.Y)(h.DW,{allowClear:!0,ariaLabel:(0,v.t)("Roles"),disabled:T,mode:"multiple",onChange:me,options:(e,t,r)=>ce("roles",e,t,r),value:(ee||[]).map((e=>({value:e.id,label:`${e.name}`})))})}),(0,k.Y)("p",{className:"help-block",children:(0,v.t)("Roles is a list which defines access to the dashboard. Granting a role access to a dashboard will bypass dataset level checks. If no roles are defined, regular access permissions apply.")})]})]}),(0,k.Y)(h.fI,{children:(0,k.Y)(h.fv,{xs:24,md:12,children:(0,k.Y)(E,{hasCustomLabelsColor:t,onChange:ge,colorScheme:q})})})]})})():(()=>{const e=pe(),t=!!Object.keys((null==e?void 0:e.label_colors)||{}).length;return(0,k.FD)(h.fI,{gutter:16,children:[(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)("h3",{style:{marginTop:"1em"},children:(0,v.t)("Access")}),(0,k.Y)(D,{label:(0,v.t)("Owners"),children:(0,k.Y)(h.DW,{allowClear:!0,ariaLabel:(0,v.t)("Owners"),disabled:T,mode:"multiple",onChange:ue,options:(e,t,r)=>ce("owners",e,t,r),value:ve()})}),(0,k.Y)("p",{className:"help-block",children:(0,v.t)("Owners is a list of users who can alter the dashboard. Searchable by name or username.")})]}),(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)("h3",{style:{marginTop:"1em"},children:(0,v.t)("Colors")}),(0,k.Y)(E,{hasCustomLabelsColor:t,onChange:ge,colorScheme:q})]})]})})(),(0,k.Y)(h.fI,{children:(0,k.Y)(h.fv,{xs:24,md:24,children:(0,k.Y)("h3",{children:(0,v.t)("Certification")})})}),(0,k.FD)(h.fI,{gutter:16,children:[(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)(D,{label:(0,v.t)("Certified by"),name:"certifiedBy",children:(0,k.Y)(n.pd,{type:"text",disabled:T})}),(0,k.Y)("p",{className:"help-block",children:(0,v.t)("Person or group that has certified this dashboard.")})]}),(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)(D,{label:(0,v.t)("Certification details"),name:"certificationDetails",children:(0,k.Y)(n.pd,{type:"text",disabled:T})}),(0,k.Y)("p",{className:"help-block",children:(0,v.t)("Any additional detail to show in the certification tooltip.")})]})]}),(0,x.G7)(x.TO.TaggingSystem)?(0,k.Y)(h.fI,{gutter:16,children:(0,k.Y)(h.fv,{xs:24,md:12,children:(0,k.Y)("h3",{css:_,children:(0,v.t)("Tags")})})}):null,(0,x.G7)(x.TO.TaggingSystem)?(0,k.Y)(h.fI,{gutter:16,children:(0,k.FD)(h.fv,{xs:24,md:12,children:[(0,k.Y)(D,{children:(0,k.Y)(h.DW,{ariaLabel:"Tags",mode:"multiple",value:oe,options:$.m,onChange:e=>{const t=(0,y.A)(e).map((e=>({id:e.value,name:e.label})));ie(t)},allowClear:!0})}),(0,k.Y)("p",{className:"help-block",children:(0,v.t)("A list of tags that have been applied to this chart.")})]})}):null,(0,k.Y)(h.fI,{children:(0,k.FD)(h.fv,{xs:24,md:24,children:[(0,k.Y)("h3",{style:{marginTop:"1em"},children:(0,k.FD)(d.A,{buttonStyle:"link",onClick:()=>B(!P),css:w.AH`
                  padding: 0;
                `,children:[(0,k.Y)("i",{className:"fa fa-angle-"+(P?"down":"right"),style:{minWidth:"1em"}}),(0,v.t)("Advanced")]})}),P&&(0,k.FD)(k.FK,{children:[(0,k.Y)(D,{label:(0,v.t)("JSON metadata"),children:(0,k.Y)(N,{showLoadingForImport:!0,name:"json_metadata",value:K,onChange:Z,tabSize:2,width:"100%",height:"200px",wrapEnabled:!0})}),(0,k.FD)("p",{className:"help-block",children:[(0,v.t)("This JSON object is generated dynamically when clicking the save or overwrite button in the dashboard view. It is exposed here for reference and for power users who may want to alter specific parameters."),F&&(0,k.FD)(k.FK,{children:[" ",(0,v.t)('Please DO NOT overwrite the "filter_scopes" key.')," ",(0,k.Y)(Y.A,{triggerNode:(0,k.Y)("span",{className:"alert-link",children:(0,v.t)('Use "%(menuName)s" menu instead.',{menuName:(0,v.t)("Set filter mapping")})})})]})]})]})]})})]})})}))},75264:(e,t,r)=>{r.d(t,{Dj:()=>a,cE:()=>n,cp:()=>o});var l=r(96453),i=r(2445);const a=()=>{const e=(0,l.DP)();return(0,i.FD)("svg",{width:"18",height:"18",viewBox:"0 0 18 18",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,i.Y)("path",{d:"M16 0H2C0.89 0 0 0.9 0 2V16C0 17.1 0.89 18 2 18H16C17.11 18 18 17.1 18 16V2C18 0.9 17.11 0 16 0Z",fill:e.colors.primary.base}),(0,i.Y)("path",{d:"M7 14L2 9L3.41 7.59L7 11.17L14.59 3.58L16 5L7 14Z",fill:"white"})]})},n=()=>{const e=(0,l.DP)();return(0,i.FD)("svg",{width:"18",height:"18",viewBox:"0 0 18 18",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,i.Y)("path",{d:"M16 0H2C0.9 0 0 0.9 0 2V16C0 17.1 0.9 18 2 18H16C17.1 18 18 17.1 18 16V2C18 0.9 17.1 0 16 0Z",fill:e.colors.grayscale.light1}),(0,i.Y)("path",{d:"M14 10H4V8H14V10Z",fill:"white"})]})},o=()=>{const e=(0,l.DP)();return(0,i.FD)("svg",{width:"18",height:"18",viewBox:"0 0 18 18",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,i.Y)("path",{d:"M16 0H2C0.9 0 0 0.9 0 2V16C0 17.1 0.9 18 2 18H16C17.1 18 18 17.1 18 16V2C18 0.9 17.1 0 16 0Z",fill:e.colors.grayscale.light2}),(0,i.Y)("path",{d:"M16 2V16H2V2H16V2Z",fill:"white"})]})}},76125:(e,t,r)=>{r.d(t,{A:()=>S});var l=r(33031),i=r.n(l),a=r(96540),n=r(78518),o=r(96453),s=r(17437),c=r(7148),d=r(63756),h=r(94963),p=r(83307),u=r(50317),m=r(19129),v=r(67073),f=r(6308),g=r(3175),b=r(55556),y=r(2445);function x(e){const{id:t,label:r,colors:l}=e,[i,n]=(0,a.useState)(!1),o=(0,a.useRef)(null),c=(0,a.useRef)(null),d=()=>l.map(((e,r)=>(0,y.Y)("span",{"data-test":"color",css:t=>s.AH`
          padding-left: ${t.gridUnit/2}px;
          :before {
            content: '';
            display: inline-block;
            background-color: ${e};
            border: 1px solid ${"white"===e?"black":e};
            width: 9px;
            height: 10px;
          }
        `},`${t}-${r}`)));return(0,y.Y)(m.m_,{"data-testid":"tooltip",overlayClassName:"color-scheme-tooltip",title:()=>(0,y.FD)(y.FK,{children:[(0,y.Y)("span",{children:r}),(0,y.Y)("div",{children:d()})]}),open:i,children:(0,y.FD)("span",{className:"color-scheme-option",onMouseEnter:()=>{const e=o.current,t=c.current;e&&t&&(e.scrollWidth>e.offsetWidth||e.scrollHeight>e.offsetHeight||t.scrollWidth>t.offsetWidth||t.scrollHeight>t.offsetHeight)&&n(!0)},onMouseLeave:()=>{n(!1)},css:s.AH`
          display: flex;
          align-items: center;
          justify-content: flex-start;
        `,"data-test":t,children:[(0,y.Y)("span",{className:"color-scheme-label",ref:o,css:e=>s.AH`
            min-width: 125px;
            padding-right: ${2*e.gridUnit}px;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
          `,children:r}),(0,y.Y)("span",{ref:c,css:e=>s.AH`
            flex: 100%;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
            padding-right: ${e.gridUnit}px;
          `,children:d()})]})},t)}const{Option:w,OptGroup:z}=p.default,C=(0,n.t)("The colors of this chart might be overridden by custom label colors of the related dashboard.\n    Check the JSON metadata in the Advanced settings."),F=(0,n.t)("The color scheme is determined by the related dashboard.\n        Edit the color scheme in the dashboard properties."),k=(0,n.t)("You are viewing this chart in a dashboard context with labels shared across multiple charts.\n        The color scheme selection is disabled."),E=(0,n.t)("You are viewing this chart in the context of a dashboard that is directly affecting its colors.\n        To edit the color scheme, open this chart outside of the dashboard."),Y=({label:e,dashboardId:t,hasSharedLabelsColor:r,hasCustomLabelsColor:l,hasDashboardColorScheme:i})=>{const a=(0,o.DP)();if(r||l||i){const n=l&&!r?C:t&&i?F:k;return(0,y.FD)(y.FK,{children:[e," ",(0,y.Y)(m.m_,{title:n,children:(0,y.Y)(v.F.WarningOutlined,{iconColor:a.colors.warning.base,css:s.AH`
              vertical-align: baseline;
            `,iconSize:"s"})})]})}return(0,y.Y)(y.FK,{children:e})},S=({hasCustomLabelsColor:e=!1,hasDashboardColorScheme:t=!1,mapLabelsColors:r={},sharedLabelsColors:l=[],dashboardId:p,colorNamespace:v,chartId:C,label:F=(0,n.t)("Color scheme"),onChange:k=()=>{},value:S,clearable:M=!1,defaultScheme:$,choices:O=[],schemes:A={},isLinear:V,...I})=>{var H;const D=l.length,N=(0,c.Ay)(),_=C&&(null==(H=N.chartsLabelsMap.get(C))?void 0:H.labels)||[],R=!!(p&&D>0&&_.some((e=>l.includes(e)))),U=p&&t,j=U||R,T=(0,o.DP)(),L=(0,a.useMemo)((()=>{if(j)return"dashboard";let e=S||$;if("SUPERSET_DEFAULT"===e){var t;const r="function"==typeof A?A():A;e=null==r||null==(t=r.SUPERSET_DEFAULT)?void 0:t.id}return e}),[$,A,j,S]),P=(0,a.useMemo)((()=>{if(j)return[(0,y.Y)(w,{value:"dashboard",label:(0,n.t)("Dashboard"),children:(0,y.Y)(m.m_,{title:E,children:(0,n.t)("Dashboard scheme")})},"dashboard")];const e="function"==typeof A?A():A,t="function"==typeof O?O():O,r=[],l=t.filter((e=>{const t=e[0],l="SUPERSET_DEFAULT"!==t&&!r.includes(t);return r.push(t),l})).reduce(((t,[r])=>{var l,i;const a=e[r];let n=[];a&&(n=V?a.getColors(10):a.colors);const o={customLabel:(0,y.Y)(x,{id:a.id,label:a.label,colors:n}),label:(null==e||null==(l=e[r])?void 0:l.label)||r,value:r};return t[null!=(i=a.group)?i:d.w.Other].options.push(o),t}),{[d.w.Custom]:{title:d.w.Custom,label:(0,n.t)("Custom color palettes"),options:[]},[d.w.Featured]:{title:d.w.Featured,label:(0,n.t)("Featured color palettes"),options:[]},[d.w.Other]:{title:d.w.Other,label:(0,n.t)("Other color palettes"),options:[]}}),a=Object.values(l).filter((e=>e.options.length>0)).map((e=>({...e,options:i()(e.options,(e=>e.label))})));return 1===a.length&&a[0].title===d.w.Other?a[0].options.map(((e,t)=>(0,y.Y)(w,{value:e.value,label:e.label,children:e.customLabel},t))):a.map(((e,t)=>(0,y.Y)(z,{label:e.label,children:e.options.map(((e,r)=>(0,y.Y)(w,{value:e.value,label:e.label,children:e.customLabel},`${t}-${r}`)))},t)))}),[O,U,R,V,A]);return(0,y.FD)(y.FK,{children:[(0,y.Y)(u.A,{...I,label:(0,y.Y)(Y,{label:F,dashboardId:p,hasCustomLabelsColor:e,hasDashboardColorScheme:t,hasSharedLabelsColor:R})}),(0,y.Y)(f.Iu,{css:s.AH`
          width: 100%;
          & .ant-select-item.ant-select-item-group {
            padding-left: ${T.gridUnit}px;
            font-size: ${T.typography.sizes.m}px;
          }
          & .ant-select-item-option-grouped {
            padding-left: ${3*T.gridUnit}px;
          }
        `,"aria-label":(0,n.t)("Select color scheme"),allowClear:M,disabled:U||R,onChange:e=>{if(C&&(N.setOwnColorScheme(C,e),p)){const e=(0,b.Z6)(v),t=h.getNamespace(e),i=new Set(l),a=Object.keys(r).filter((e=>!i.has(e)));t.resetColorsForLabels(a)}k(e)},placeholder:(0,n.t)("Select scheme"),value:L,getPopupContainer:e=>e.parentNode,showSearch:!0,filterOption:(e,t)=>(0,g.qY)(e,t,["label","value"],!0),children:P})]})}},93103:(e,t,r)=>{r.d(t,{LO:()=>p,R2:()=>u,ms:()=>m});var l=r(96540),i=r(45572),a=r(96453),n=r(67073),o=r(2445);const s=a.I4.div`
  width: ${({theme:e})=>.75*e.gridUnit}px;
  height: ${({theme:e})=>.75*e.gridUnit}px;
  border-radius: 50%;
  background-color: ${({theme:e})=>e.colors.grayscale.light1};

  font-weight: ${({theme:e})=>e.typography.weights.normal};
  display: inline-flex;
  position: relative;

  &:hover {
    background-color: ${({theme:e})=>e.colors.primary.base};

    &::before,
    &::after {
      background-color: ${({theme:e})=>e.colors.primary.base};
    }
  }

  &::before,
  &::after {
    position: absolute;
    content: ' ';
    width: ${({theme:e})=>.75*e.gridUnit}px;
    height: ${({theme:e})=>.75*e.gridUnit}px;
    border-radius: 50%;
    background-color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  &::before {
    top: ${({theme:e})=>e.gridUnit}px;
  }

  &::after {
    bottom: ${({theme:e})=>e.gridUnit}px;
  }
`,c=a.I4.div`
  display: flex;
  align-items: center;
  padding: ${({theme:e})=>2*e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`;var d;!function(e){e.Vertical="vertical",e.Horizontal="horizontal"}(d||(d={}));const h=(e=d.Vertical)=>e===d.Horizontal?(0,o.Y)(n.F.EllipsisOutlined,{iconSize:"xl"}):(0,o.Y)(s,{}),p=({overlay:e,iconOrientation:t=d.Vertical,...r})=>(0,o.Y)(i.A,{dropdownRender:()=>e,...r,children:(0,o.Y)(c,{"data-test":"dropdown-trigger",children:h(t)})}),u=e=>{const{children:t,onBlur:r,onKeyDown:a,...n}=e,s=(0,l.cloneElement)(t,{onBlur:r,onKeyDown:a});return(0,o.Y)(i.A,{autoFocus:!0,overlayStyle:e.overlayStyle,...n,children:s})},m=e=>(0,o.Y)(i.A,{autoFocus:!0,...e})},94704:(e,t,r)=>{r.d(t,{A:()=>h});var l=r(96540),i=r(96453),a=r(17437),n=r(78518),o=r(19129),s=r(67073),c=r(2445);const d=i.I4.a`
  ${({theme:e})=>a.AH`
    font-size: ${e.typography.sizes.xl}px;
    display: flex;
    padding: 0 0 0 ${2*e.gridUnit}px;
  `};
`,h=({itemId:e,isStarred:t,showTooltip:r,saveFaveStar:a,fetchFaveStar:h})=>{const p=(0,i.DP)();(0,l.useEffect)((()=>{null==h||h(e)}),[h,e]);const u=(0,l.useCallback)((r=>{r.preventDefault(),a(e,!!t)}),[t,e,a]),m=(0,c.Y)(d,{href:"#",onClick:u,className:"fave-unfave-icon","data-test":"fave-unfave-icon",role:"button",children:t?(0,c.Y)(s.F.StarFilled,{"aria-label":"starred",iconSize:"l",iconColor:p.colors.warning.base}):(0,c.Y)(s.F.StarOutlined,{"aria-label":"unstarred",iconSize:"l",iconColor:p.colors.grayscale.light1})});return r?(0,c.Y)(o.m_,{id:"fave-unfave-tooltip",title:(0,n.t)("Click to favorite/unfavorite"),children:m}):m}},97567:(e,t,r)=>{r.d(t,{FA:()=>s,Ik:()=>h,dH:()=>d,iQ:()=>o,un:()=>c});var l=r(35742),i=r(58561),a=r.n(i);const n=Object.freeze(["dashboard","chart","saved_query"]),o=Object.freeze({DASHBOARD:"dashboard",CHART:"chart",QUERY:"saved_query"});function s(e,t,r){l.A.get({endpoint:`/api/v1/tag/${e}`}).then((({json:e})=>t(e.result))).catch((e=>r(e)))}function c({objectType:e,objectId:t,includeTypes:r=!1},i,a){if(void 0===e||void 0===t)throw new Error("Need to specify objectType and objectId");if(!n.includes(e))throw new Error(`objectType ${e} is invalid`);l.A.get({endpoint:`/api/v1/${e}/${t}`}).then((({json:e})=>i(e.result.tags.filter((e=>1===e.type))))).catch((e=>a(e)))}function d(e,t,r){const i=e.map((e=>e.name));l.A.delete({endpoint:`/api/v1/tag/?q=${a().encode(i)}`}).then((({json:e})=>e.message?t(e.message):t("Successfully Deleted Tag"))).catch((e=>{const t=e.message;return r(t||"Error Deleting Tag")}))}function h({tagIds:e=[],types:t},r,i){let a=`/api/v1/tag/get_objects/?tagIds=${e}`;t&&(a+=`&types=${t}`),l.A.get({endpoint:a}).then((({json:e})=>r(e.result))).catch((e=>i(e)))}}}]);