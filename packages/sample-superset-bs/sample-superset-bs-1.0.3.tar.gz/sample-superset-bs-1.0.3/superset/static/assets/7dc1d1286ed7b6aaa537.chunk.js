"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[8968],{11188:(e,t,a)=>{a.d(t,{A:()=>g});var s=a(96453),r=a(78518),n=a(78360),i=a(69633),l=a(8143),o=a(69172),d=a(10286),c=a(45738),u=a(67073),h=a(73135),p=a(2445);c.A.registerLanguage("sql",n.A),c.A.registerLanguage("markdown",l.A),c.A.registerLanguage("html",i.A),c.A.registerLanguage("json",o.A);const m=s.I4.div`
  margin-top: -24px;

  &:hover {
    svg {
      visibility: visible;
    }
  }

  svg {
    position: relative;
    top: 40px;
    left: 512px;
    visibility: hidden;
    margin: -4px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`;function g({addDangerToast:e,addSuccessToast:t,children:a,...s}){return(0,p.FD)(m,{children:[(0,p.Y)(u.F.CopyOutlined,{tabIndex:0,role:"button",onClick:s=>{var n;s.preventDefault(),s.currentTarget.blur(),n=a,(0,h.A)((()=>Promise.resolve(n))).then((()=>{t&&t((0,r.t)("SQL Copied!"))})).catch((()=>{e&&e((0,r.t)("Sorry, your browser does not support copying."))}))}}),(0,p.Y)(c.A,{style:d.A,...s,children:a})]})}},12397:(e,t,a)=>{a.d(t,{U:()=>l});var s=a(19129),r=a(25106),n=a(78518),i=a(2445);const l=({user:e,date:t})=>{const a=(0,i.Y)("span",{className:"no-wrap","data-test":"audit-info-date",children:t});if(e){const t=(0,r.A)(e),l=(0,n.t)("Modified by: %s",t);return(0,i.Y)(s.m_,{title:l,placement:"bottom",children:a})}return a}},14318:(e,t,a)=>{a.d(t,{A:()=>r});var s=a(96540);function r({queries:e,fetchData:t,currentQueryId:a}){const r=e.findIndex((e=>e.id===a)),[n,i]=(0,s.useState)(r),[l,o]=(0,s.useState)(!1),[d,c]=(0,s.useState)(!1);function u(){o(0===n),c(n===e.length-1)}function h(a){const s=n+(a?-1:1);s>=0&&s<e.length&&(t(e[s].id),i(s),u())}return(0,s.useEffect)((()=>{u()})),{handleKeyPress:function(t){n>=0&&n<e.length&&("ArrowDown"===t.key||"k"===t.key?(t.preventDefault(),h(!1)):"ArrowUp"!==t.key&&"j"!==t.key||(t.preventDefault(),h(!0)))},handleDataChange:h,disablePrevious:l,disableNext:d}}},25143:(e,t,a)=>{a.d(t,{S:()=>s.A,v:()=>r.A});var s=a(46740),r=a(16707)},64535:(e,t,a)=>{a.d(t,{A:()=>n});var s=a(66265),r=a(2445);const n=e=>(0,r.Y)(s.A,{...e})},67733:(e,t,a)=>{a.r(t),a.d(t,{default:()=>j});var s=a(78518),r=a(96453),n=a(35742),i=a(17437),l=a(27366),o=a(96540),d=a(61574),c=a(71519),u=a(58561),h=a.n(u),p=a(30703),m=a(61225),g=a(64535),y=a(5261),b=a(50500),v=a(63358),w=a(4780),f=a(51713),S=a(43849),x=a(17444),_=a(37020),A=a(83691),q=a(25143),k=a(19129),T=a(93514),F=a(23193),Y=a(74354),D=a(12397),C=a(3932),$=a(67073),N=a(85861),P=a(46920),I=a(11188),H=a(14318),O=a(2445);const E=r.I4.div`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  margin-bottom: 0;
`,L=r.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
  padding: 4px 0 16px 0;
`,K=(0,r.I4)(N.Ay)`
  .antd5-modal-body {
    padding: 24px;
  }

  pre {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
    font-weight: ${({theme:e})=>e.typography.weights.normal};
    line-height: ${({theme:e})=>e.typography.sizes.l}px;
    height: 375px;
    border: none;
  }
`,U=(0,y.Ay)((({fetchData:e,onHide:t,openInSqlLab:a,queries:r,savedQuery:n,show:i,addDangerToast:l,addSuccessToast:o})=>{const{handleKeyPress:d,handleDataChange:c,disablePrevious:u,disableNext:h}=(0,H.A)({queries:r,currentQueryId:n.id,fetchData:e});return(0,O.Y)("div",{role:"none",onKeyUp:d,children:(0,O.FD)(K,{onHide:t,show:i,title:(0,s.t)("Query preview"),footer:(0,O.FD)(O.FK,{children:[(0,O.Y)(P.A,{"data-test":"previous-saved-query",disabled:u,onClick:()=>c(!0),children:(0,s.t)("Previous")},"previous-saved-query"),(0,O.Y)(P.A,{"data-test":"next-saved-query",disabled:h,onClick:()=>c(!1),children:(0,s.t)("Next")},"next-saved-query"),(0,O.Y)(P.A,{"data-test":"open-in-sql-lab",buttonStyle:"primary",onClick:({metaKey:e})=>a(n.id,Boolean(e)),children:(0,s.t)("Open in SQL Lab")},"open-in-sql-lab")]}),children:[(0,O.Y)(E,{children:(0,s.t)("Query name")}),(0,O.Y)(L,{children:n.label}),(0,O.Y)(I.A,{language:"sql",addDangerToast:l,addSuccessToast:o,children:n.sql||""})]})})}));var z=a(84666);const R=(0,s.t)('The passwords for the databases below are needed in order to import them together with the saved queries. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),Q=(0,s.t)("You are importing one or more saved queries that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),B=r.I4.div`
  .count {
    margin-left: 5px;
    color: ${({theme:e})=>e.colors.primary.base};
    text-decoration: underline;
    cursor: pointer;
  }
`,M=r.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
`,j=(0,y.Ay)((function({addDangerToast:e,addSuccessToast:t,user:a}){const u=(0,r.DP)(),{state:{loading:y,resourceCount:N,resourceCollection:P,bulkSelectEnabled:I},hasPerm:H,fetchData:E,toggleBulkSelect:L,refreshData:K}=(0,b.RU)("saved_query",(0,s.t)("Saved queries"),e),{roles:j}=(0,m.d4)((e=>e.user)),J=(0,z.L)("can_read","Tag",j),[W,V]=(0,o.useState)(null),[G,X]=(0,o.useState)(null),[Z,ee]=(0,o.useState)(!1),[te,ae]=(0,o.useState)([]),[se,re]=(0,o.useState)(!1),[ne,ie]=(0,o.useState)([]),[le,oe]=(0,o.useState)([]),[de,ce]=(0,o.useState)([]),ue=(0,d.W6)(),he=H("can_write"),pe=H("can_write"),me=H("can_write"),ge=H("can_export"),ye=(0,o.useCallback)((t=>{n.A.get({endpoint:`/api/v1/saved_query/${t}`}).then((({json:e={}})=>{X({...e.result})}),(0,p.JF)((t=>e((0,s.t)("There was an issue previewing the selected query %s",t)))))}),[e]),be={activeChild:"Saved queries",...T.F},ve=[];me&&ve.push({name:(0,s.t)("Bulk select"),onClick:L,buttonStyle:"secondary"}),ve.push({name:(0,O.FD)(c.N_,{to:"/sqllab?new=true",css:i.AH`
          display: flex;
          &:hover {
            color: currentColor;
            text-decoration: none;
          }
        `,children:[(0,O.Y)($.F.PlusOutlined,{iconColor:u.colors.primary.light5,iconSize:"m",css:i.AH`
            margin: auto ${2*u.gridUnit}px auto 0;
          `}),(0,s.t)("Query")]}),buttonStyle:"primary"}),he&&ve.push({name:(0,O.Y)(k.m_,{id:"import-tooltip",title:(0,s.t)("Import queries"),placement:"bottomRight","data-test":"import-tooltip-test",children:(0,O.Y)($.F.DownloadOutlined,{"data-test":"import-icon"})}),buttonStyle:"link",onClick:()=>{ee(!0)},"data-test":"import-button"}),be.buttons=ve;const we=(e,t)=>{t?window.open(`/sqllab?savedQueryId=${e}`):ue.push(`/sqllab?savedQueryId=${e}`)},fe=(0,o.useCallback)((async a=>{try{const e={dbId:a.db_id,name:a.label,schema:a.schema,catalog:a.catalog,sql:a.sql,autorun:!1,templateParams:null},r=await n.A.post({endpoint:"/api/v1/sqllab/permalink",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)}),{url:i}=r.json;await navigator.clipboard.writeText(i),t((0,s.t)("Link Copied!"))}catch(t){e((0,s.t)("There was an error generating the permalink."))}}),[e,t]),Se=e=>{const t=e.map((({id:e})=>e));(0,w.A)("saved_query",t,(()=>{re(!1)})),re(!0)},xe=[{id:"changed_on_delta_humanized",desc:!0}],_e=(0,o.useMemo)((()=>[{accessor:"label",Header:(0,s.t)("Name"),Cell:({row:{original:{id:e,label:t}}})=>(0,O.Y)(c.N_,{to:`/sqllab?savedQueryId=${e}`,children:t})},{accessor:"description",Header:(0,s.t)("Description")},{accessor:"database.database_name",Header:(0,s.t)("Database"),size:"xl"},{accessor:"database",hidden:!0,disableSortBy:!0},{accessor:"schema",Header:(0,s.t)("Schema"),size:"xl"},{Cell:({row:{original:{sql_tables:e=[]}}})=>{const t=e.map((e=>e.table)),a=(null==t?void 0:t.shift())||"";return t.length?(0,O.FD)(B,{children:[(0,O.Y)("span",{children:a}),(0,O.Y)(g.A,{placement:"right",title:(0,s.t)("TABLES"),trigger:"click",content:(0,O.Y)(O.FK,{children:t.map((e=>(0,O.Y)(M,{children:e},e)))}),children:(0,O.FD)("span",{className:"count",children:["(+",t.length,")"]})})]}):a},accessor:"sql_tables",Header:(0,s.t)("Tables"),size:"xl",disableSortBy:!0},{Cell:({row:{original:{tags:e=[]}}})=>(0,O.Y)(q.S,{tags:e.filter((e=>1===e.type))}),Header:(0,s.t)("Tags"),accessor:"tags",disableSortBy:!0,hidden:!(0,l.G7)(l.TO.TaggingSystem)},{Cell:({row:{original:{changed_by:e,changed_on_delta_humanized:t}}})=>(0,O.Y)(D.U,{user:e,date:t}),Header:(0,s.t)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>{const t=[{label:"preview-action",tooltip:(0,s.t)("Query preview"),placement:"bottom",icon:"Binoculars",onClick:()=>{ye(e.id)}},pe&&{label:"edit-action",tooltip:(0,s.t)("Edit query"),placement:"bottom",icon:"EditOutlined",onClick:({metaKey:t})=>we(e.id,Boolean(t))},{label:"copy-action",tooltip:(0,s.t)("Copy query URL"),placement:"bottom",icon:"CopyOutlined",onClick:()=>fe(e)},ge&&{label:"export-action",tooltip:(0,s.t)("Export query"),placement:"bottom",icon:"UploadOutlined",onClick:()=>Se([e])},me&&{label:"delete-action",tooltip:(0,s.t)("Delete query"),placement:"bottom",icon:"DeleteOutlined",onClick:()=>V(e)}].filter((e=>!!e));return(0,O.Y)(A.A,{actions:t})},Header:(0,s.t)("Actions"),id:"actions",disableSortBy:!0},{accessor:F.H.ChangedBy,hidden:!0}]),[me,pe,ge,fe,ye]),Ae=(0,o.useMemo)((()=>[{Header:(0,s.t)("Search"),id:"label",key:"search",input:"search",operator:S.t.AllText,toolTipDescription:"Searches all text fields: Name, Description, Database & Schema"},{Header:(0,s.t)("Database"),key:"database",id:"database",input:"select",operator:S.t.RelationOneMany,unfilteredLabel:(0,s.t)("All"),fetchSelects:(0,p.u1)("saved_query","database",(0,p.JF)((t=>e((0,s.t)("An error occurred while fetching dataset datasource values: %s",t))))),paginate:!0},{Header:(0,s.t)("Schema"),id:"schema",key:"schema",input:"select",operator:S.t.Equals,unfilteredLabel:"All",fetchSelects:(0,p.$C)("saved_query","schema",(0,p.JF)((t=>e((0,s.t)("An error occurred while fetching schema values: %s",t))))),paginate:!0},...(0,l.G7)(l.TO.TaggingSystem)&&J?[{Header:(0,s.t)("Tag"),id:"tags",key:"tags",input:"select",operator:S.t.SavedQueryTagById,fetchSelects:C.m}]:[],{Header:(0,s.t)("Modified by"),key:"changed_by",id:"changed_by",input:"select",operator:S.t.RelationOneMany,unfilteredLabel:(0,s.t)("All"),fetchSelects:(0,p.u1)("saved_query","changed_by",(0,p.JF)((e=>(0,s.t)("An error occurred while fetching dataset datasource values: %s",e))),a),paginate:!0}]),[e]);return(0,O.FD)(O.FK,{children:[(0,O.Y)(f.A,{...be}),W&&(0,O.Y)(_.A,{description:(0,s.t)("This action will permanently delete the saved query."),onConfirm:()=>{W&&(({id:a,label:r})=>{n.A.delete({endpoint:`/api/v1/saved_query/${a}`}).then((()=>{K(),V(null),t((0,s.t)("Deleted: %s",r))}),(0,p.JF)((t=>e((0,s.t)("There was an issue deleting %s: %s",r,t)))))})(W)},onHide:()=>V(null),open:!0,title:(0,s.t)("Delete Query?")}),G&&(0,O.Y)(U,{fetchData:ye,onHide:()=>X(null),savedQuery:G,queries:P,openInSqlLab:we,show:!0}),(0,O.Y)(v.A,{title:(0,s.t)("Please confirm"),description:(0,s.t)("Are you sure you want to delete the selected queries?"),onConfirm:a=>{n.A.delete({endpoint:`/api/v1/saved_query/?q=${h().encode(a.map((({id:e})=>e)))}`}).then((({json:e={}})=>{K(),t(e.message)}),(0,p.JF)((t=>e((0,s.t)("There was an issue deleting the selected queries: %s",t)))))},children:a=>{const r=[];return me&&r.push({key:"delete",name:(0,s.t)("Delete"),onSelect:a,type:"danger"}),ge&&r.push({key:"export",name:(0,s.t)("Export"),type:"primary",onSelect:Se}),(0,O.Y)(S.A,{className:"saved_query-list-view",columns:_e,count:N,data:P,fetchData:E,filters:Ae,initialSort:xe,loading:y,pageSize:25,bulkActions:r,addSuccessToast:t,addDangerToast:e,bulkSelectEnabled:I,disableBulkSelect:L,highlightRowId:null==G?void 0:G.id,enableBulkTag:!0,bulkTagResourceName:"query",refreshData:K})}}),(0,O.Y)(Y.A,{resourceName:"saved_query",resourceLabel:(0,s.t)("queries"),passwordsNeededMessage:R,confirmOverwriteMessage:Q,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{ee(!1),K(),t((0,s.t)("Query imported"))},show:Z,onHide:()=>{ee(!1)},passwordFields:te,setPasswordFields:ae,sshTunnelPasswordFields:ne,setSSHTunnelPasswordFields:ie,sshTunnelPrivateKeyFields:le,setSSHTunnelPrivateKeyFields:oe,sshTunnelPrivateKeyPasswordFields:de,setSSHTunnelPrivateKeyPasswordFields:ce}),se&&(0,O.Y)(x.A,{})]})}))},74354:(e,t,a)=>{a.d(t,{A:()=>m});var s=a(96540),r=a(96453),n=a(78518),i=a(46920),l=a(85861),o=a(15595),d=a(50500),c=a(31383),u=a(2445);const h=r.I4.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,p=r.I4.div`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
  padding-top: ${({theme:e})=>2*e.gridUnit}px;

  & > div {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${({theme:e})=>3*e.gridUnit}px;
    }
  }
`,m=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:r,onModelImport:m,show:g,onHide:y,passwordFields:b=[],setPasswordFields:v=()=>{},sshTunnelPasswordFields:w=[],setSSHTunnelPasswordFields:f=()=>{},sshTunnelPrivateKeyFields:S=[],setSSHTunnelPrivateKeyFields:x=()=>{},sshTunnelPrivateKeyPasswordFields:_=[],setSSHTunnelPrivateKeyPasswordFields:A=()=>{}})=>{const[q,k]=(0,s.useState)(!0),[T,F]=(0,s.useState)({}),[Y,D]=(0,s.useState)(!1),[C,$]=(0,s.useState)(!1),[N,P]=(0,s.useState)([]),[I,H]=(0,s.useState)(!1),[O,E]=(0,s.useState)(),[L,K]=(0,s.useState)({}),[U,z]=(0,s.useState)({}),[R,Q]=(0,s.useState)({}),B=()=>{P([]),v([]),F({}),D(!1),$(!1),H(!1),E(""),f([]),x([]),A([]),K({}),z({}),Q({})},{state:{alreadyExists:M,passwordsNeeded:j,sshPasswordNeeded:J,sshPrivateKeyNeeded:W,sshPrivateKeyPasswordNeeded:V},importResource:G}=(0,d.bN)(e,t,(e=>{E(e)}));(0,s.useEffect)((()=>{v(j),j.length>0&&H(!1)}),[j,v]),(0,s.useEffect)((()=>{D(M.length>0),M.length>0&&H(!1)}),[M,D]),(0,s.useEffect)((()=>{f(J),J.length>0&&H(!1)}),[J,f]),(0,s.useEffect)((()=>{x(W),W.length>0&&H(!1)}),[W,x]),(0,s.useEffect)((()=>{A(V),V.length>0&&H(!1)}),[V,A]);return q&&g&&k(!1),(0,u.FD)(l.Ay,{name:"model",className:"import-model-modal",disablePrimaryButton:0===N.length||Y&&!C||I,onHandledPrimaryAction:()=>{var e;(null==(e=N[0])?void 0:e.originFileObj)instanceof File&&(H(!0),G(N[0].originFileObj,T,L,U,R,C).then((e=>{e&&(B(),m())})))},onHide:()=>{k(!0),y(),B()},primaryButtonName:Y?(0,n.t)("Overwrite"):(0,n.t)("Import"),primaryButtonType:Y?"danger":"primary",width:"750px",show:g,title:(0,u.Y)("h4",{children:(0,n.t)("Import %s",t)}),children:[(0,u.Y)(p,{children:(0,u.Y)(o._O,{name:"modelFile",id:"modelFile","data-test":"model-file-input",accept:".yaml,.json,.yml,.zip",fileList:N,onChange:e=>{P([{...e.file,status:"done"}])},onRemove:e=>(P(N.filter((t=>t.uid!==e.uid))),!1),customRequest:()=>{},disabled:I,children:(0,u.Y)(i.A,{loading:I,children:(0,n.t)("Select file")})})}),O&&(0,u.Y)(c.A,{errorMessage:O,showDbInstallInstructions:b.length>0||w.length>0||S.length>0||_.length>0}),(()=>{if(0===b.length&&0===w.length&&0===S.length&&0===_.length)return null;const e=[...new Set([...b,...w,...S,..._])];return(0,u.FD)(u.FK,{children:[(0,u.Y)("h5",{children:(0,n.t)("Database passwords")}),(0,u.Y)(h,{children:a}),e.map((e=>(0,u.FD)(u.FK,{children:[(null==b?void 0:b.indexOf(e))>=0&&(0,u.FD)(p,{children:[(0,u.FD)("div",{className:"control-label",children:[(0,n.t)("%s PASSWORD",e.slice(10)),(0,u.Y)("span",{className:"required",children:"*"})]}),(0,u.Y)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:T[e],onChange:t=>F({...T,[e]:t.target.value})})]},`password-for-${e}`),(null==w?void 0:w.indexOf(e))>=0&&(0,u.FD)(p,{children:[(0,u.FD)("div",{className:"control-label",children:[(0,n.t)("%s SSH TUNNEL PASSWORD",e.slice(10)),(0,u.Y)("span",{className:"required",children:"*"})]}),(0,u.Y)("input",{name:`ssh_tunnel_password-${e}`,autoComplete:`ssh_tunnel_password-${e}`,type:"password",value:L[e],onChange:t=>K({...L,[e]:t.target.value}),"data-test":"ssh_tunnel_password"})]},`ssh_tunnel_password-for-${e}`),(null==S?void 0:S.indexOf(e))>=0&&(0,u.FD)(p,{children:[(0,u.FD)("div",{className:"control-label",children:[(0,n.t)("%s SSH TUNNEL PRIVATE KEY",e.slice(10)),(0,u.Y)("span",{className:"required",children:"*"})]}),(0,u.Y)("textarea",{name:`ssh_tunnel_private_key-${e}`,autoComplete:`ssh_tunnel_private_key-${e}`,value:U[e],onChange:t=>z({...U,[e]:t.target.value}),"data-test":"ssh_tunnel_private_key"})]},`ssh_tunnel_private_key-for-${e}`),(null==_?void 0:_.indexOf(e))>=0&&(0,u.FD)(p,{children:[(0,u.FD)("div",{className:"control-label",children:[(0,n.t)("%s SSH TUNNEL PRIVATE KEY PASSWORD",e.slice(10)),(0,u.Y)("span",{className:"required",children:"*"})]}),(0,u.Y)("input",{name:`ssh_tunnel_private_key_password-${e}`,autoComplete:`ssh_tunnel_private_key_password-${e}`,type:"password",value:R[e],onChange:t=>Q({...R,[e]:t.target.value}),"data-test":"ssh_tunnel_private_key_password"})]},`ssh_tunnel_private_key_password-for-${e}`)]})))]})})(),Y?(0,u.Y)(u.FK,{children:(0,u.FD)(p,{children:[(0,u.Y)("div",{className:"confirm-overwrite",children:r}),(0,u.Y)("div",{className:"control-label",children:(0,n.t)('Type "%s" to confirm',(0,n.t)("OVERWRITE"))}),(0,u.Y)("input",{"data-test":"overwrite-modal-input",id:"overwrite",type:"text",onChange:e=>{var t,a;const s=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";$(s.toUpperCase()===(0,n.t)("OVERWRITE"))}})]})}):null]})}},83691:(e,t,a)=>{a.d(t,{A:()=>d});var s=a(96453),r=a(19129),n=a(67073),i=a(2445);const l=s.I4.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:e})=>e.colors.primary.base};
      }
    }
  }
`,o=s.I4.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function d({actions:e}){return(0,i.Y)(l,{className:"actions",children:e.map(((e,t)=>{const a=n.F[e.icon];return e.tooltip?(0,i.Y)(r.m_,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,children:(0,i.Y)(o,{role:"button",tabIndex:0,className:"action-button","data-test":e.label,onClick:e.onClick,children:(0,i.Y)(a,{iconSize:"l"})})},t):(0,i.Y)(o,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,"data-test":e.label,children:(0,i.Y)(a,{})},t)}))})}},93514:(e,t,a)=>{a.d(t,{F:()=>r});var s=a(78518);const r={name:(0,s.t)("SQL"),tabs:[{name:"Saved queries",label:(0,s.t)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:(0,s.t)("Query history"),url:"/sqllab/history/",usesRouter:!0}]}}}]);