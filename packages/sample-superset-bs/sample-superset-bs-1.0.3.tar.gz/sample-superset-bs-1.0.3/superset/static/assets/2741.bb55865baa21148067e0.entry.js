"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2741],{19980:(e,a,t)=>{t.d(a,{A:()=>R});var n=t(96540),l=t(35742),r=t(51436),i=t(78518),o=t(85861),s=t(46920),d=t(75488),c=t(61693),h=t(15595),u=t(67073),p=t(90868),m=t(58561),g=t.n(m),b=t(5261),v=t(40563),f=t(96453),_=t(17437);const y=(0,f.I4)(v.eI)`
  ${({theme:e})=>_.AH`
    flex: 1;
    margin-top: 0;
    margin-bottom: ${2.5*e.gridUnit}px;
  }
  `}
`,x=f.I4.div`
  display: flex;
  align-items: center;
  margin-top: 0;
`,Y=_.AH`
  .antd5-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,w=e=>_.AH`
  .switch-label {
    color: ${e.colors.grayscale.base};
    margin-left: ${4*e.gridUnit}px;
  }
`,C=e=>_.AH`
  .antd5-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .antd5-modal-close-x .close {
    opacity: 1;
  }

  .antd5-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .antd5-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }

  .info-solid-small {
    vertical-align: bottom;
  }
`;var S=t(46740),A=t(2445);const D=f.I4.div`
  //margin-top: 10px;
  //margin-bottom: 10px;
`,F=({columns:e,maxColumnsToShow:a=4})=>{const t=e.map((e=>({name:e})));return(0,A.FD)(D,{children:[(0,A.Y)(h.o5.Text,{type:"secondary",children:"Columns:"}),0===e.length?(0,A.Y)("p",{className:"help-block",children:(0,i.t)("Upload file to preview columns")}):(0,A.Y)(S.A,{tags:t,maxTags:a})]})};var k=t(31641);const $=({label:e,tip:a,children:t,name:n,rules:l})=>(0,A.Y)(y,{label:(0,A.FD)("div",{children:[e,(0,A.Y)(k.A,{tooltip:a})]}),name:n,rules:l,children:t}),N=["delimiter","skip_initial_space","skip_blank_lines","day_first","column_data_types","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],E=["sheet_name","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],I=[],T=["rows_to_read","index_column"],U=[...N,...E,...I],q={csv:N,excel:E,columnar:I},P=(e,a)=>q[a].includes(e),O={table_name:"",schema:"",sheet_name:void 0,delimiter:",",already_exists:"fail",skip_initial_space:!1,skip_blank_lines:!1,day_first:!1,decimal_character:".",null_values:[],header_row:"0",rows_to_read:null,skip_rows:"0",column_dates:[],index_column:null,dataframe_index:!1,index_label:"",columns_read:[],column_data_types:""},L={csv:".csv, .tsv",excel:".xls, .xlsx",columnar:".parquet, .zip"},M={csv:"CSV",excel:"Excel",columnar:"Columnar"},H=({label:e,dataTest:a,children:t,...n})=>(0,A.FD)(x,{children:[(0,A.Y)(d.d,{"data-test":a,...n}),(0,A.Y)("div",{className:"switch-label",children:e}),t]}),R=(0,b.Ay)((({addDangerToast:e,addSuccessToast:a,onHide:t,show:d,allowedExtensions:m,type:b="csv"})=>{const[v]=h.Wq.useForm(),[f,x]=(0,n.useState)(0),[S,D]=(0,n.useState)([]),[k,N]=(0,n.useState)([]),[E,I]=(0,n.useState)([]),[R,z]=(0,n.useState)({}),[j,B]=(0,n.useState)(","),[V,K]=(0,n.useState)(!1),[W,Q]=(0,n.useState)(),[J,G]=(0,n.useState)(!1),[X,Z]=(0,n.useState)(!0),[ee,ae]=(0,n.useState)(!1),te=(0,n.useMemo)((()=>(e="",a,t)=>{const n=g().encode_uri({filters:[{col:"allow_file_upload",opr:"eq",value:!0}],page:a,page_size:t});return l.A.get({endpoint:`/api/v1/database/?q=${n}`}).then((e=>({data:e.json.result.map((e=>({value:e.id,label:e.database_name}))),totalCount:e.json.count})))}),[]),ne=(0,n.useMemo)((()=>(e="",a,t)=>f?l.A.get({endpoint:`/api/v1/database/${f}/schemas/?q=(upload_allowed:!t)`}).then((e=>({data:e.json.result.map((e=>({value:e,label:e}))),totalCount:e.json.count}))):Promise.resolve({data:[],totalCount:0})),[f]),le=a=>{const t=v.getFieldsValue(),n={...O,...t},i=new FormData;return i.append("file",a),"csv"===b&&i.append("delimiter",n.delimiter),i.append("type",b),ae(!0),l.A.post({endpoint:"/api/v1/database/upload_metadata/",body:i,headers:{Accept:"application/json"}}).then((e=>{const{items:a}=e.json.result;if(a&&"excel"!==b)N(a[0].column_names);else{const{allSheetNames:e,sheetColumnNamesMap:t}=a.reduce(((e,a)=>(e.allSheetNames.push(a.sheet_name),e.sheetColumnNamesMap[a.sheet_name]=a.column_names,e)),{allSheetNames:[],sheetColumnNamesMap:{}});N(a[0].column_names),I(e),v.setFieldsValue({sheet_name:e[0]}),z(t)}})).catch((a=>(0,r.h4)(a).then((a=>{e(a.error||"Error"),N([]),v.setFieldsValue({sheet_name:void 0}),I([])})))).finally((()=>{ae(!1)}))},re=()=>{D([]),N([]),Q(""),x(0),I([]),K(!1),B(","),Z(!0),ae(!1),z({}),v.resetFields(),t()},ie=()=>k.map((e=>({value:e,label:e})));(0,n.useEffect)((()=>{if(k.length>0&&S[0].originFileObj&&S[0].originFileObj instanceof File){if(!X)return;le(S[0].originFileObj).then((e=>e))}}),[j]);const oe={csv:(0,i.t)("CSV upload"),excel:(0,i.t)("Excel upload"),columnar:(0,i.t)("Columnar upload")};return(0,A.Y)(o.Ay,{css:e=>[Y,C(e),w(e)],primaryButtonLoading:V,name:"database","data-test":"upload-modal",onHandledPrimaryAction:v.submit,onHide:re,width:"500px",primaryButtonName:"Upload",centered:!0,show:d,title:(0,A.Y)((()=>{const e=oe[b]||(0,i.t)("Upload");return(0,A.Y)("h4",{children:e})}),{}),children:(0,A.Y)(h.Wq,{form:v,onFinish:()=>{var t;const n=v.getFieldsValue();delete n.database,n.schema=W;const o={...O,...n},s=new FormData,d=null==(t=S[0])?void 0:t.originFileObj;d&&s.append("file",d),((e,a)=>{const t=(()=>{const e=q[b]||[];return[...U].filter((a=>!e.includes(a)))})();Object.entries(a).forEach((([a,n])=>{t.includes(a)||T.includes(a)&&null==n||e.append(a,n)}))})(s,o),K(!0);const c=`/api/v1/database/${f}/upload/`;return s.append("type",b),l.A.post({endpoint:c,body:s,headers:{Accept:"application/json"}}).then((()=>{a((0,i.t)("Data imported")),K(!1),re()})).catch((a=>(0,r.h4)(a).then((a=>{e(a.error||"Error")})))).finally((()=>{K(!1)}))},"data-test":"dashboard-edit-properties-form",layout:"vertical",initialValues:O,children:(0,A.FD)(c.A,{expandIconPosition:"right",accordion:!0,defaultActiveKey:"general",css:e=>(e=>_.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;
    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.s}px;
    }
  }
  h4 {
    font-size: ${e.typography.sizes.l}px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("General information")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Upload a file to a database.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{label:(0,i.t)("%(label)s file",{label:M[b]}),name:"file",required:!0,rules:[{validator:(e,a)=>0===S.length?Promise.reject((0,i.t)("Uploading a file is required")):((e,a)=>{const t=e.name.match(/.+\.([^.]+)$/);if(!t)return!1;const n=t[1].toLowerCase();return a.map((e=>e.toLowerCase())).includes(n)})(S[0],m)?Promise.resolve():Promise.reject((0,i.t)("Upload a file with a valid extension. Valid: [%s]",m.join(",")))}],children:(0,A.Y)(h._O,{name:"modelFile",id:"modelFile","data-test":"model-file-input",accept:L[b],fileList:S,onChange:async e=>{D([{...e.file,status:"done"}]),X&&await le(e.file.originFileObj)},onRemove:e=>(D(S.filter((a=>a.uid!==e.uid))),N([]),I([]),v.setFieldsValue({sheet_name:void 0}),!1),customRequest:()=>{},children:(0,A.Y)(s.A,{"aria-label":(0,i.t)("Select"),icon:(0,A.Y)(u.F.UploadOutlined,{}),loading:ee,children:(0,i.t)("Select")})})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{children:(0,A.Y)(H,{label:(0,i.t)("Preview uploaded file"),dataTest:"previewUploadedFile",onChange:e=>{Z(e)},checked:X})})})}),X&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{columns:k})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{label:(0,i.t)("Database"),required:!0,name:"database",rules:[{validator:(e,a)=>f?Promise.resolve():Promise.reject((0,i.t)("Selecting a database is required"))}],children:(0,A.Y)(h.DW,{ariaLabel:(0,i.t)("Select a database"),options:te,onChange:e=>{x(null==e?void 0:e.value),Q(void 0),v.setFieldsValue({schema:void 0})},allowClear:!0,placeholder:(0,i.t)("Select a database to upload the file to")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{label:(0,i.t)("Schema"),name:"schema",children:(0,A.Y)(h.DW,{ariaLabel:(0,i.t)("Select a schema"),options:ne,onChange:e=>{Q(null==e?void 0:e.value)},allowClear:!0,placeholder:(0,i.t)("Select a schema if the database supports this")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{label:(0,i.t)("Table name"),name:"table_name",required:!0,rules:[{required:!0,message:"Table name is required"}],children:(0,A.Y)(p.pd,{"aria-label":(0,i.t)("Table Name"),name:"table_name","data-test":"properties-modal-name-input",type:"text",placeholder:(0,i.t)("Name of table to be created")})})})}),P("delimiter",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)($,{label:(0,i.t)("Delimiter"),tip:(0,i.t)("Select a delimiter for this data"),name:"delimiter",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose a delimiter"),options:[{value:",",label:'Comma ","'},{value:";",label:'Semicolon ";"'},{value:"\t",label:'Tab "\\t"'},{value:"|",label:"Pipe"}],onChange:e=>{B(e)},allowNewOptions:!0})})})}),P("sheet_name",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{label:(0,i.t)("Sheet name"),name:"sheet_name",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose sheet name"),options:E.map((e=>({value:e,label:e}))),onChange:e=>{var a;N(null!=(a=R[e])?a:[])},allowNewOptions:!0,placeholder:(0,i.t)("Select a sheet name from the uploaded file")})})})})]},"general"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("File settings")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Adjust how spaces, blank lines, null values are handled and other file wide settings.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)($,{label:(0,i.t)("If table already exists"),tip:(0,i.t)("What should happen if the table already exists"),name:"already_exists",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose already exists"),options:[{value:"fail",label:"Fail"},{value:"replace",label:"Replace"},{value:"append",label:"Append"}],onChange:()=>{}})})})}),P("column_dates",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{label:(0,i.t)("Columns to be parsed as dates"),name:"column_dates",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose columns to be parsed as dates"),mode:"multiple",options:ie(),allowClear:!0,allowNewOptions:!0,placeholder:(0,i.t)("Select column names from a dropdown list that should be parsed as dates.")})})})}),P("decimal_character",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)($,{label:(0,i.t)("Decimal character"),tip:(0,i.t)("Character to interpret as decimal point"),name:"decimal_character",children:(0,A.Y)(p.pd,{type:"text"})})})}),P("null_values",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)($,{label:(0,i.t)("Null Values"),tip:(0,i.t)("Choose values that should be treated as null. Warning: Hive database supports only a single value"),name:"null_values",children:(0,A.Y)(h.l6,{mode:"multiple",options:[{value:'""',label:'Empty Strings ""'},{value:"None",label:"None"},{value:"nan",label:"nan"},{value:"null",label:"null"},{value:"N/A",label:"N/A"}],allowClear:!0,allowNewOptions:!0})})})}),P("skip_initial_space",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{name:"skip_initial_space",children:(0,A.Y)(H,{label:(0,i.t)("Skip spaces after delimiter"),dataTest:"skipInitialSpace"})})})}),P("skip_blank_lines",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{name:"skip_blank_lines",children:(0,A.Y)(H,{label:(0,i.t)("Skip blank lines rather than interpreting them as Not A Number values"),dataTest:"skipBlankLines"})})})}),P("day_first",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{name:"day_first",children:(0,A.Y)(H,{label:(0,i.t)("DD/MM format dates, international and European format"),dataTest:"dayFirst"})})})})]},"2"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("Columns")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Adjust column settings such as specifying the columns to read, how duplicates are handled, column data types, and more.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{label:(0,i.t)("Columns to read"),name:"columns_read",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose columns to read"),mode:"multiple",options:ie(),allowClear:!0,allowNewOptions:!0,placeholder:(0,i.t)("List of the column names that should be read")})})})}),P("column_data_types",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)($,{label:(0,i.t)("Column data types"),tip:(0,i.t)('A dictionary with column names and their data types if you need to change the defaults. Example: {"user_id":"int"}. Check Python\'s Pandas library for supported data types.'),name:"column_data_types",children:(0,A.Y)(p.pd,{"aria-label":(0,i.t)("Column data types"),type:"text"})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(y,{name:"dataframe_index",children:(0,A.Y)(H,{label:(0,i.t)("Create dataframe index"),dataTest:"dataFrameIndex",onChange:G})})})}),J&&P("index_column",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)($,{label:(0,i.t)("Index column"),tip:(0,i.t)("Column to use as the index of the dataframe. If None is given, Index label is used."),name:"index_column",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose index column"),options:k.map((e=>({value:e,label:e}))),allowClear:!0,allowNewOptions:!0})})})}),J&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)($,{label:(0,i.t)("Index label"),tip:(0,i.t)("Label for the index column. Don't use an existing column name."),name:"index_label",children:(0,A.Y)(p.pd,{"aria-label":(0,i.t)("Index label"),type:"text"})})})})]},"3"),P("header_row",b)&&P("rows_to_read",b)&&P("skip_rows",b)&&(0,A.Y)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("Rows")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Set header rows and the number of rows to read or skip.")})]}),children:(0,A.FD)(h.fI,{children:[(0,A.Y)(h.fv,{span:8,children:(0,A.Y)($,{label:(0,i.t)("Header row"),tip:(0,i.t)("Row containing the headers to use as column names (0 is first line of data)."),name:"header_row",rules:[{required:!0,message:"Header row is required"}],children:(0,A.Y)(p.YI,{"aria-label":(0,i.t)("Header row"),type:"text",min:0})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)($,{label:(0,i.t)("Rows to read"),tip:(0,i.t)("Number of rows of file to read. Leave empty (default) to read all rows"),name:"rows_to_read",children:(0,A.Y)(p.YI,{"aria-label":(0,i.t)("Rows to read"),min:1})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)($,{label:(0,i.t)("Skip rows"),tip:(0,i.t)("Number of rows to skip at start of file."),name:"skip_rows",rules:[{required:!0,message:"Skip rows is required"}],children:(0,A.Y)(p.YI,{"aria-label":(0,i.t)("Skip rows"),min:0})})})]})},"4")]})})})}))},31383:(e,a,t)=>{t.d(a,{A:()=>c});var n=t(78518),l=t(50500),r=t(25946),i=t(17437),o=t(2445);const s=(0,l.xK)(),d=s?s.support:"https://superset.apache.org/docs/databases/installing-database-drivers",c=({errorMessage:e,showDbInstallInstructions:a})=>(0,o.Y)(r.A,{closable:!1,css:e=>(e=>i.AH`
  margin: ${4*e.gridUnit}px 0;

  .antd5-alert-message {
    margin: 0;
  }
`)(e),type:"error",showIcon:!0,message:e,description:a?(0,o.FD)(o.FK,{children:[(0,o.Y)("br",{}),(0,n.t)("Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions: "),(0,o.Y)("a",{href:d,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,n.t)("here")}),"."]}):""})},43293:(e,a,t)=>{t.d(a,{hT:()=>Ge,Ay:()=>ea});var n=t(44383),l=t.n(n),r=t(62193),i=t.n(r),o=t(72391),s=t(96453),d=t(78518),c=t(17437),h=t(96540),u=t(61574),p=t(62221),m=t(48327),g=t(15595),b=t(25946),v=t(85861),f=t(46920),_=t(19129),y=t(91162),x=t(67073),Y=t(2445);const w=({buttonText:e,icon:a,altText:t,...n})=>(0,Y.Y)(y.A,{hoverable:!0,role:"button",tabIndex:0,"aria-label":e,onKeyDown:e=>{"Enter"!==e.key&&" "!==e.key||(n.onClick&&n.onClick(e)," "===e.key&&e.preventDefault()),null==n.onKeyDown||n.onKeyDown(e)},cover:a?(0,Y.Y)("img",{src:a,alt:t||e,css:c.AH`
          width: 100%;
          height: 120px;
          object-fit: contain;
        `}):(0,Y.Y)("div",{css:c.AH`
          display: flex;
          align-content: center;
          align-items: center;
          height: 120px;
        `,children:(0,Y.Y)(x.F.DatabaseOutlined,{css:c.AH`
            font-size: 48px;
          `,"aria-label":"default-icon"})}),css:e=>({padding:3*e.gridUnit,textAlign:"center",...n.style}),...n,children:(0,Y.Y)(_.m_,{title:e,children:(0,Y.Y)(g.o5.Text,{ellipsis:!0,children:e})})});var C,S,A=t(31641),D=t(5261),F=t(97987),k=t(79427),$=t(31383),N=t(50500),E=t(28292),I=t(17444);!function(e){e.SqlalchemyUri="sqlalchemy_form",e.DynamicForm="dynamic_form"}(C||(C={})),function(e){e.GSheet="gsheets",e.BigQuery="bigquery",e.Snowflake="snowflake"}(S||(S={}));var T=t(46942),U=t.n(T),q=t(27366),P=t(85994),O=t(61693),L=t(24976);const M=c.AH`
  margin-bottom: 0;
`,H=s.I4.header`
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  .subheader-text {
    line-height: ${({theme:e})=>4.25*e.gridUnit}px;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,R=c.AH`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,z=c.AH`
  .antd5-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,j=e=>c.AH`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
  display: flex;
`,B=e=>c.AH`
  padding-left: ${2*e.gridUnit}px;
  padding-right: ${2*e.gridUnit}px;
`,V=e=>c.AH`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,K=e=>c.AH`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .antd5-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .antd5-modal-close-x .close {
    opacity: 1;
  }

  .antd5-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .antd5-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,W=e=>c.AH`
  margin: ${4*e.gridUnit}px 0;
`,Q=s.I4.div`
  ${({theme:e})=>c.AH`
    margin: 0 ${4*e.gridUnit}px ${4*e.gridUnit}px;
  `}
`,J=e=>c.AH`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    text-align: left;
  }
`,G=e=>c.AH`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 480px;
  }
`,X=e=>c.AH`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
    margin-bottom: 0;
  }
`,Z=s.I4.div`
  ${({theme:e})=>c.AH`
    margin-bottom: ${6*e.gridUnit}px;
    &.mb-0 {
      margin-bottom: 0;
    }
    &.mb-8 {
      margin-bottom: ${2*e.gridUnit}px;
    }

    .control-label {
      color: ${e.colors.grayscale.dark1};
      font-size: ${e.typography.sizes.s}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    &.extra-container {
      padding-top: ${2*e.gridUnit}px;
    }

    .input-container {
      display: flex;
      align-items: top;

      label {
        display: flex;
        margin-left: ${2*e.gridUnit}px;
        margin-top: ${.75*e.gridUnit}px;
        font-family: ${e.typography.families.sansSerif};
        font-size: ${e.typography.sizes.m}px;
      }

      i {
        margin: 0 ${e.gridUnit}px;
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
      color: ${e.colors.grayscale.light1};
    }

    textarea,
    input[type='text'],
    input[type='number'] {
      padding: ${1.5*e.gridUnit}px ${2*e.gridUnit}px;
      border-style: none;
      border: 1px solid ${e.colors.grayscale.light2};
      border-radius: ${e.gridUnit}px;

      &[name='name'] {
        flex: 0 1 auto;
        width: 40%;
      }
    }
    &.expandable {
      height: 0;
      overflow: hidden;
      transition: height 0.25s;
      margin-left: ${8*e.gridUnit}px;
      margin-bottom: 0;
      padding: 0;
      .control-label {
        margin-bottom: 0;
      }
      &.open {
        height: ${108}px;
        padding-right: ${5*e.gridUnit}px;
      }
    }
  `}
`,ee=(0,s.I4)(L.iN)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,ae=s.I4.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${261}px;
      &.ctas-open {
        height: ${363}px;
      }
    }
  }
`,te=s.I4.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,ne=e=>c.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,le=e=>c.AH`
  font-size: ${3.5*e.gridUnit}px;
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,re=s.I4.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0px;
  }
`,ie=(s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`),oe=s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,se=s.I4.div`
  .catalog-type-select {
    margin: 0 0 20px;
  }

  .label-select {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>4*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    width: 100%;

    button {
      width: fit-content;
    }

    .credentials-uploaded {
      display: flex;
      align-items: center;
      gap: ${({theme:e})=>3*e.gridUnit}px;
      width: fit-content;
    }

    .credentials-uploaded-btn, .credentials-uploaded-remove {
      flex: 0 0 auto;
    }

    /* hide native file upload input element */
    .input-upload {
      display: none !important;
    }
  }`,de=s.I4.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>e.typography.sizes.l}px;
      font-weight: ${({theme:e})=>e.typography.weights.bold};
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,ce=(0,s.I4)(f.A)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,he=s.I4.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
  height: auto;
`,ue=s.I4.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 20px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    font-weight: ${({theme:e})=>e.typography.weights.bold};
    margin: ${({theme:e})=>10*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 7px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
      margin-bottom: 0px;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-add-btn {
    width: 95%;
  }
`,pe=s.I4.div`
  .ant-progress-inner {
    display: none;
  }

  .ant-upload-list-item-card-actions {
    display: none;
  }
`,me=({db:e,onInputChange:a,onTextChange:t,onEditorChange:n,onExtraInputChange:l,onExtraEditorChange:r,extraExtension:i})=>{var o,h,u,p,m;const g=!(null==e||!e.expose_in_sqllab),b=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas),v=null==e||null==(o=e.engine_information)?void 0:o.supports_file_upload,f=null==e||null==(h=e.engine_information)?void 0:h.supports_dynamic_catalog,_=JSON.parse((null==e?void 0:e.extra)||"{}",((e,a)=>"engine_params"===e&&"object"==typeof a?JSON.stringify(a):a)),y=(0,s.DP)(),x=null==i?void 0:i.component,w=null==i?void 0:i.logo,C=null==i?void 0:i.description,S=!!(0,q.G7)(q.TO.ForceSqlLabRunAsync)||!(null==e||!e.allow_run_async),D=(0,q.G7)(q.TO.ForceSqlLabRunAsync);return(0,Y.FD)(O.A,{expandIconPosition:"right",accordion:!0,css:e=>(e=>c.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,Y.Y)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("SQL Lab")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Adjust how this database will interact with SQL Lab.")})]}),children:(0,Y.FD)(Z,{css:M,children:[(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:a,labelText:(0,d.t)("Expose database in SQL Lab")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow this database to be queried in SQL Lab")})]}),(0,Y.FD)(ae,{className:U()("expandable",{open:g,"ctas-open":b}),children:[(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:a,labelText:(0,d.t)("Allow CREATE TABLE AS")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow creation of new tables based on queries")})]})}),(0,Y.FD)(Z,{css:M,children:[(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:a,labelText:(0,d.t)("Allow CREATE VIEW AS")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow creation of new views based on queries")})]}),(0,Y.FD)(Z,{className:U()("expandable",{open:b}),children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("CTAS & CVAS SCHEMA")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"force_ctas_schema",placeholder:(0,d.t)("Create or select schema..."),onChange:a,value:(null==e?void 0:e.force_ctas_schema)||""})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")})]})]}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:a,labelText:(0,d.t)("Allow DDL and DML")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Allow the execution of DDL (Data Definition Language: CREATE, DROP, TRUNCATE, etc.) and DML (Data Modification Language: INSERT, UPDATE, DELETE, etc)")})]})}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==_||!_.cost_estimate_enabled),onChange:l,labelText:(0,d.t)("Enable query cost estimation")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("For Bigquery, Presto and Postgres, shows a button to compute cost before running a query.")})]})}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!1!==(null==_?void 0:_.allows_virtual_table_explore),onChange:l,labelText:(0,d.t)("Allow this database to be explored")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("When enabled, users are able to visualize SQL Lab results in Explore.")})]})}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"disable_data_preview",indeterminate:!1,checked:!(null==_||!_.disable_data_preview),onChange:l,labelText:(0,d.t)("Disable SQL Lab data preview queries")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Disable data preview when fetching table metadata in SQL Lab.  Useful to avoid browser performance issues when using  databases with very wide tables.")})]})}),(0,Y.Y)(Z,{children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"expand_rows",indeterminate:!1,checked:!(null==_||null==(u=_.schema_options)||!u.expand_rows),onChange:l,labelText:(0,d.t)("Enable row expansion in schemas")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("For Trino, describe full schemas of nested ROW types, expanding them with dotted paths")})]})})]})]})},"1"),(0,Y.FD)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("Performance")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Adjust performance settings of this database.")})]}),children:[(0,Y.FD)(Z,{className:"mb-8",children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Chart cache timeout")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:a})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires, and -1 bypasses the cache. Note this defaults to the global timeout if undefined.")})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Schema cache timeout")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"number",name:"schema_cache_timeout",value:(null==_||null==(p=_.metadata_cache_timeout)?void 0:p.schema_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l,"data-test":"schema-cache-timeout-test"})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires.")})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Table cache timeout")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"number",name:"table_cache_timeout",value:(null==_||null==(m=_.metadata_cache_timeout)?void 0:m.table_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l,"data-test":"table-cache-timeout-test"})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. ")})]}),(0,Y.Y)(Z,{css:(0,c.AH)({no_margin_bottom:M},"",""),children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"allow_run_async",indeterminate:!1,checked:S,onChange:a,labelText:(0,d.t)("Asynchronous query execution")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}),D&&(0,Y.Y)(A.A,{iconStyle:{color:y.colors.error.base},tooltip:(0,d.t)("This option has been disabled by the administrator.")})]})}),(0,Y.Y)(Z,{css:(0,c.AH)({no_margin_bottom:M},"",""),children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==_||!_.cancel_query_on_windows_unload),onChange:l,labelText:(0,d.t)("Cancel query on window unload event")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})]})})]},"2"),(0,Y.FD)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("Security")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Add extra connection information.")})]}),children:[(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Secure extra")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(ee,{name:"masked_encrypted_extra",value:(null==e?void 0:e.masked_encrypted_extra)||"",placeholder:(0,d.t)("Secure extra"),onChange:e=>n({json:e,name:"masked_encrypted_extra"}),width:"100%",height:"160px"})}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")})})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Root certificate")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:(0,d.t)("Enter CA_BUNDLE"),onChange:t})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines.")})]}),(0,Y.Y)(Z,{css:v?{}:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:a,labelText:(0,d.t)("Impersonate logged in user (Presto, Trino, Drill, Hive, and GSheets)")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")})]})}),v&&(0,Y.Y)(Z,{css:null!=e&&e.allow_file_upload?{}:M,children:(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(P.A,{id:"allow_file_upload",indeterminate:!1,checked:!(null==e||!e.allow_file_upload),onChange:a,labelText:(0,d.t)("Allow file uploads to database")})})}),v&&!(null==e||!e.allow_file_upload)&&(0,Y.FD)(Z,{css:M,children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Schemas allowed for File upload")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"schemas_allowed_for_file_upload",value:((null==_?void 0:_.schemas_allowed_for_file_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:l})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("A comma-separated list of schemas that files are allowed to upload to.")})]})]},"3"),i&&x&&C&&(0,Y.Y)(O.A.Panel,{header:(0,Y.FD)("div",{children:[w&&(0,Y.Y)(w,{}),(0,Y.Y)("span",{css:e=>({fontSize:e.typography.sizes.l,fontWeight:e.typography.weights.bold}),children:null==i?void 0:i.title}),(0,Y.Y)("p",{className:"helper",children:(0,Y.Y)(C,{})})]}),collapsible:null!=i.enabled&&i.enabled()?"icon":"disabled",children:(0,Y.Y)(Z,{css:M,children:(0,Y.Y)(x,{db:e,onEdit:i.onEdit})})},null==i?void 0:i.title),(0,Y.FD)(O.A.Panel,{header:(0,Y.FD)("div",{children:[(0,Y.Y)("h4",{children:(0,d.t)("Other")}),(0,Y.Y)("p",{className:"helper",children:(0,d.t)("Additional settings.")})]}),children:[(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Metadata Parameters")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(ee,{name:"metadata_params",placeholder:(0,d.t)("Metadata Parameters"),onChange:e=>r({json:e,name:"metadata_params"}),width:"100%",height:"160px",value:Object.keys((null==_?void 0:_.metadata_params)||{}).length?null==_?void 0:_.metadata_params:""})}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")})})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Engine Parameters")}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)(ee,{name:"engine_params",placeholder:(0,d.t)("Engine Parameters"),onChange:e=>r({json:e,name:"engine_params"}),width:"100%",height:"160px",value:Object.keys((null==_?void 0:_.engine_params)||{}).length?null==_?void 0:_.engine_params:""})}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")})})]}),(0,Y.FD)(Z,{children:[(0,Y.Y)("div",{className:"control-label","data-test":"version-label-test",children:(0,d.t)("Version")}),(0,Y.Y)("div",{className:"input-container","data-test":"version-spinbutton-test",children:(0,Y.Y)("input",{type:"text",name:"version",placeholder:(0,d.t)("Version number"),onChange:l,value:(null==_?void 0:_.version)||""})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Specify the database version. This is used with Presto for query cost estimation, and Dremio for syntax changes, among others.")})]}),(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"disable_drill_to_detail",indeterminate:!1,checked:!(null==_||!_.disable_drill_to_detail),onChange:l,labelText:(0,d.t)("Disable drill to detail")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Disables the drill to detail feature for this database.")})]})}),f&&(0,Y.Y)(Z,{css:M,children:(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(P.A,{id:"allow_multi_catalog",indeterminate:!1,checked:!(null==_||!_.allow_multi_catalog),onChange:l,labelText:(0,d.t)("Allow changing catalogs")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Give access to multiple catalogs in a single database connection.")})]})})]},"4")]})};var ge=t(27588);const be=({db:e,onInputChange:a,testConnection:t,conf:n,testInProgress:l=!1,children:r})=>{var i,o;const s=(null==ge.A||null==(i=ge.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:i.SQLALCHEMY_DOCS_URL)||"https://docs.sqlalchemy.org/en/13/core/engines.html",h=(null==ge.A||null==(o=ge.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:o.SQLALCHEMY_DISPLAY_TEXT)||"SQLAlchemy docs";return(0,Y.FD)(Y.FK,{children:[(0,Y.FD)(Z,{children:[(0,Y.FD)("div",{className:"control-label",children:[(0,d.t)("Display Name"),(0,Y.Y)("span",{className:"required",children:"*"})]}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"database_name","data-test":"database-name-input",value:(null==e?void 0:e.database_name)||"",placeholder:(0,d.t)("Name your database"),onChange:a})}),(0,Y.Y)("div",{className:"helper",children:(0,d.t)("Pick a name to help you identify this database.")})]}),(0,Y.FD)(Z,{children:[(0,Y.FD)("div",{className:"control-label",children:[(0,d.t)("SQLAlchemy URI"),(0,Y.Y)("span",{className:"required",children:"*"})]}),(0,Y.Y)("div",{className:"input-container",children:(0,Y.Y)("input",{type:"text",name:"sqlalchemy_uri","data-test":"sqlalchemy-uri-input",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:(null==e?void 0:e.sqlalchemy_uri_placeholder)||(0,d.t)("dialect+driver://username:password@host:port/database"),onChange:a})}),(0,Y.FD)("div",{className:"helper",children:[(0,d.t)("Refer to the")," ",(0,Y.Y)("a",{href:s||(null==n?void 0:n.SQLALCHEMY_DOCS_URL)||"",target:"_blank",rel:"noopener noreferrer",children:h||(null==n?void 0:n.SQLALCHEMY_DISPLAY_TEXT)||""})," ",(0,d.t)("for more information on how to structure your URI.")]})]}),r,(0,Y.Y)(f.A,{onClick:t,loading:l,cta:!0,buttonStyle:"link",css:e=>(e=>c.AH`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`)(e),children:(0,d.t)("Test connection")})]})};var ve=t(40563),fe=t(75488),_e=t(90868);const ye=e=>c.AH`
  .ant-collapse-header {
    padding-bottom: ${1.5*e.gridUnit}px !important;
    padding-top: ${1.5*e.gridUnit}px !important;
  }
  .anticon.ant-collapse-arrow {
    top: 0 !important;
  }
`,xe={account:{label:"Account",helpText:(0,d.t)("Copy the identifier of the account you are trying to connect to."),placeholder:(0,d.t)("e.g. xy12345.us-east-2.aws")},warehouse:{label:"Warehouse",placeholder:(0,d.t)("e.g. compute_wh"),className:"form-group-w-50"},role:{label:"Role",placeholder:(0,d.t)("e.g. AccountAdmin"),className:"form-group-w-50"}},Ye=({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,field:r})=>{var i,o;return(0,Y.Y)(F.A,{id:r,name:r,required:e,value:null==l||null==(i=l.parameters)?void 0:i[r],validationMethods:{onBlur:t},errorMessage:null==n?void 0:n[r],placeholder:xe[r].placeholder,helpText:null==(o=xe[r])?void 0:o.helpText,label:xe[r].label||r,onChange:a.onParametersChange,className:xe[r].className||r})};var we,Ce=t(40458);!function(e){e[e.JsonUpload=0]="JsonUpload",e[e.CopyPaste=1]="CopyPaste"}(we||(we={}));const Se={gsheets:"service_account_info",bigquery:"credentials_info"},Ae=({changeMethods:e,isEditMode:a,db:t,editNewDb:n})=>{var l;const r=(0,h.useRef)(null),[i,o]=(0,h.useState)(we.JsonUpload.valueOf()),[s,c]=(0,h.useState)(null),u=!a,p=(null==t?void 0:t.engine)&&Se[t.engine],m=null==t||null==(l=t.parameters)?void 0:l[p],b=m&&"object"==typeof m?JSON.stringify(m):m;return(0,Y.FD)(se,{children:[u&&(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ce.A,{children:(0,d.t)("How do you want to enter service account credentials?")}),(0,Y.FD)(g._P,{defaultValue:i,style:{width:"100%"},onChange:e=>o(e),children:[(0,Y.Y)(g._P.Option,{value:we.JsonUpload,children:(0,d.t)("Upload JSON file")}),(0,Y.Y)(g._P.Option,{value:we.CopyPaste,children:(0,d.t)("Copy and Paste JSON credentials")})]})]}),i===we.CopyPaste||a||n?(0,Y.FD)("div",{className:"input-container",children:[(0,Y.Y)(Ce.A,{children:(0,d.t)("Service Account")}),(0,Y.Y)("textarea",{className:"input-form",name:p,value:"boolean"==typeof b?String(b):b,onChange:e.onParametersChange,placeholder:(0,d.t)("Paste content of service credentials JSON file here")})]}):u&&(0,Y.FD)("div",{className:"input-container",css:e=>j(e),children:[!s&&(0,Y.FD)(g.$n,{onClick:()=>{var e;return null==(e=r.current)?void 0:e.click()},children:[(0,Y.Y)(x.F.LinkOutlined,{iconSize:"m"}),(0,d.t)("Upload credentials")]}),s&&(0,Y.FD)("div",{className:"credentials-uploaded",children:[(0,Y.FD)(g.$n,{block:!0,disabled:!0,children:[(0,Y.Y)(x.F.LinkOutlined,{iconSize:"m"}),(0,d.t)("Credentials uploaded")]}),(0,Y.Y)(x.F.DeleteFilled,{iconSize:"m",onClick:()=>{c(null),e.onParametersChange({target:{name:p,value:""}})}})]}),(0,Y.Y)("input",{ref:r,id:"selectedFile",accept:".json",className:"input-upload",type:"file",onChange:async a=>{var t,n;let l;a.target.files&&(l=a.target.files[0]),c(null==(t=l)?void 0:t.name),e.onParametersChange({target:{type:null,name:p,value:await(null==(n=l)?void 0:n.text()),checked:!1}}),r.current&&(r.current.value=null)}})]})]})},De=({clearValidationErrors:e,changeMethods:a,db:t,dbModel:n})=>{var l,r,o;const[s,c]=(0,h.useState)(!1),u=(0,q.G7)(q.TO.SshTunneling),p=(null==n||null==(l=n.engine_information)?void 0:l.disable_ssh_tunneling)||!1,m=u&&!p;return(0,h.useEffect)((()=>{var e;m&&void 0!==(null==t||null==(e=t.parameters)?void 0:e.ssh)&&c(t.parameters.ssh)}),[null==t||null==(r=t.parameters)?void 0:r.ssh,m]),(0,h.useEffect)((()=>{var e;m&&void 0===(null==t||null==(e=t.parameters)?void 0:e.ssh)&&!i()(null==t?void 0:t.ssh_tunnel)&&a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:!0}})}),[a,null==t||null==(o=t.parameters)?void 0:o.ssh,null==t?void 0:t.ssh_tunnel,m]),m?(0,Y.FD)("div",{css:e=>j(e),children:[(0,Y.Y)(fe.d,{checked:s,onChange:t=>{c(t),a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:t}}),e()},"data-test":"ssh-tunnel-switch"}),(0,Y.Y)("span",{css:B,children:(0,d.t)("SSH Tunnel")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("SSH Tunnel configuration parameters"),placement:"right",viewBox:"0 -5 24 24"})]}):null};var Fe;const ke=["host","port","database","default_catalog","default_schema","username","password","access_token","http_path","http_path_field","database_name","project_id","catalog","credentials_info","service_account_info","query","encryption","account","warehouse","role","ssh","oauth2_client_info"],$e={host:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(F.A,{id:"host",name:"host",value:null==l||null==(r=l.parameters)?void 0:r.host,required:e,hasTooltip:!0,tooltipText:(0,d.t)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.host,placeholder:(0,d.t)("e.g. 127.0.0.1"),className:"form-group-w-50",label:(0,d.t)("Host"),onChange:a.onParametersChange})},http_path:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r,i;const o=JSON.parse((null==l?void 0:l.extra)||"{}");return(0,Y.Y)(F.A,{id:"http_path",name:"http_path",required:e,value:null==(r=o.engine_params)||null==(i=r.connect_args)?void 0:i.http_path,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onExtraInputChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},http_path_field:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(F.A,{id:"http_path_field",name:"http_path_field",required:e,value:null==l||null==(r=l.parameters)?void 0:r.http_path_field,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},port:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(Y.FK,{children:(0,Y.Y)(F.A,{id:"port",name:"port",type:"number",required:e,value:null==l||null==(r=l.parameters)?void 0:r.port,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.port,placeholder:(0,d.t)("e.g. 5432"),className:"form-group-w-50",label:(0,d.t)("Port"),onChange:a.onParametersChange})})},database:({required:e,changeMethods:a,getValidation:t,validationErrors:n,placeholder:l,db:r})=>{var i;return(0,Y.Y)(F.A,{id:"database",name:"database",required:e,value:null==r||null==(i=r.parameters)?void 0:i.database,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.database,placeholder:null!=l?l:(0,d.t)("e.g. world_population"),label:(0,d.t)("Database name"),onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the database you are trying to connect to.")})},default_catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(F.A,{id:"default_catalog",name:"default_catalog",required:e,value:null==l||null==(r=l.parameters)?void 0:r.default_catalog,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_catalog,placeholder:(0,d.t)("e.g. hive_metastore"),label:(0,d.t)("Default Catalog"),onChange:a.onParametersChange,helpText:(0,d.t)("The default catalog that should be used for the connection.")})},default_schema:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(F.A,{id:"default_schema",name:"default_schema",required:e,value:null==l||null==(r=l.parameters)?void 0:r.default_schema,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_schema,placeholder:(0,d.t)("e.g. default"),label:(0,d.t)("Default Schema"),onChange:a.onParametersChange,helpText:(0,d.t)("The default schema that should be used for the connection.")})},username:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,Y.Y)(F.A,{id:"username",name:"username",required:e,value:null==l||null==(r=l.parameters)?void 0:r.username,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.username,placeholder:(0,d.t)("e.g. Analytics"),label:(0,d.t)("Username"),onChange:a.onParametersChange})},password:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:r})=>{var i;return(0,Y.Y)(F.A,{id:"password",name:"password",required:e,visibilityToggle:!r,value:null==l||null==(i=l.parameters)?void 0:i.password,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.password,placeholder:(0,d.t)("e.g. ********"),label:(0,d.t)("Password"),onChange:a.onParametersChange})},oauth2_client_info:({changeMethods:e,db:a,default_value:t})=>{var n,l,r,i,o;const s=JSON.parse((null==a?void 0:a.masked_encrypted_extra)||"{}"),[d,c]=(0,h.useState)({id:(null==(n=s.oauth2_client_info)?void 0:n.id)||"",secret:(null==(l=s.oauth2_client_info)?void 0:l.secret)||"",authorization_request_uri:(null==(r=s.oauth2_client_info)?void 0:r.authorization_request_uri)||(null==t?void 0:t.authorization_request_uri)||"",token_request_uri:(null==(i=s.oauth2_client_info)?void 0:i.token_request_uri)||(null==t?void 0:t.token_request_uri)||"",scope:(null==(o=s.oauth2_client_info)?void 0:o.scope)||(null==t?void 0:t.scope)||""}),u=a=>t=>{const n={...d,[a]:t.target.value};c(n);const l={target:{type:"object",name:"oauth2_client_info",value:n}};e.onParametersChange(l)};return(0,Y.Y)(O.A,{children:(0,Y.FD)(O.A.Panel,{header:"OAuth2 client information",css:ye,children:[(0,Y.Y)(ve.eI,{label:"Client ID",children:(0,Y.Y)(_e.pd,{"data-test":"client-id",value:d.id,onChange:u("id")})}),(0,Y.Y)(ve.eI,{label:"Client Secret",children:(0,Y.Y)(_e.pd,{"data-test":"client-secret",type:"password",value:d.secret,onChange:u("secret")})}),(0,Y.Y)(ve.eI,{label:"Authorization Request URI",children:(0,Y.Y)(_e.pd,{"data-test":"client-authorization-request-uri",placeholder:"https://",value:d.authorization_request_uri,onChange:u("authorization_request_uri")})}),(0,Y.Y)(ve.eI,{label:"Token Request URI",children:(0,Y.Y)(_e.pd,{"data-test":"client-token-request-uri",placeholder:"https://",value:d.token_request_uri,onChange:u("token_request_uri")})}),(0,Y.Y)(ve.eI,{label:"Scope",children:(0,Y.Y)(_e.pd,{"data-test":"client-scope",value:d.scope,onChange:u("scope")})})]},"1")})},access_token:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:r,default_value:i,description:o})=>{var s;return(0,Y.Y)(F.A,{id:"access_token",name:"access_token",required:e,visibilityToggle:!r,value:null==l||null==(s=l.parameters)?void 0:s.access_token,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.access_token,placeholder:(0,d.t)("Paste your access token here"),get_url:"string"==typeof i&&i.includes("https://")?i:null,description:o,label:(0,d.t)("Access token"),onChange:a.onParametersChange})},database_name:({changeMethods:e,getValidation:a,validationErrors:t,db:n})=>(0,Y.Y)(Y.FK,{children:(0,Y.Y)(F.A,{id:"database_name",name:"database_name",required:!0,value:null==n?void 0:n.database_name,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.database_name,placeholder:"",label:(0,d.t)("Display Name"),onChange:e.onChange,helpText:(0,d.t)("Pick a nickname for how the database will display in Superset.")})}),query:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>(0,Y.Y)(F.A,{id:"query_input",name:"query_input",required:e,value:(null==l?void 0:l.query_input)||"",validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.query,placeholder:(0,d.t)("e.g. param1=value1&param2=value2"),label:(0,d.t)("Additional Parameters"),onChange:a.onQueryChange,helpText:(0,d.t)("Add additional custom parameters")}),encryption:({isEditMode:e,changeMethods:a,db:t,sslForced:n})=>{var l;return(0,Y.FD)("div",{css:e=>j(e),children:[(0,Y.Y)(fe.d,{disabled:n&&!e,checked:(null==t||null==(l=t.parameters)?void 0:l.encryption)||n,onChange:e=>{a.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),(0,Y.Y)("span",{css:B,children:"SSL"}),(0,Y.Y)(A.A,{tooltip:(0,d.t)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"})]})},credentials_info:Ae,service_account_info:Ae,catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{const r=(null==l?void 0:l.catalog)||[],i=n||{};return(0,Y.FD)(ue,{children:[(0,Y.Y)("h4",{className:"gsheet-title",children:(0,d.t)("Connect Google Sheets as tables to this database")}),(0,Y.FD)("div",{children:[null==r?void 0:r.map(((n,l)=>{var o,s;return(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ce.A,{className:"catalog-label",children:(0,d.t)("Google Sheet Name and URL")}),(0,Y.FD)("div",{className:"catalog-name",children:[(0,Y.Y)(F.A,{className:"catalog-name-input",required:e,validationMethods:{onBlur:t},errorMessage:null==(o=i[l])?void 0:o.name,placeholder:(0,d.t)("Enter a name for this sheet"),onChange:e=>{a.onParametersChange({target:{type:`catalog-${l}`,name:"name",value:e.target.value}})},value:n.name}),(null==r?void 0:r.length)>1&&(0,Y.Y)(x.F.CloseOutlined,{css:e=>c.AH`
                    align-self: center;
                    background: ${e.colors.grayscale.light4};
                    margin: 5px 5px 8px 5px;

                    &.anticon > * {
                      line-height: 0;
                    }
                  `,iconSize:"m",onClick:()=>a.onRemoveTableCatalog(l)})]}),(0,Y.Y)(F.A,{className:"catalog-name-url",required:e,validationMethods:{onBlur:t},errorMessage:null==(s=i[l])?void 0:s.url,placeholder:(0,d.t)("Paste the shareable Google Sheet URL here"),onChange:e=>a.onParametersChange({target:{type:`catalog-${l}`,name:"value",value:e.target.value}}),value:n.value})]})})),(0,Y.FD)(ce,{className:"catalog-add-btn",onClick:()=>{a.onAddTableCatalog()},children:["+ ",(0,d.t)("Add sheet")]})]}),(0,Y.Y)("div",{className:"helper",children:(0,Y.Y)("div",{children:(0,d.t)("In order to connect to non-public sheets you need to either provide a service account or configure an OAuth2 client.")})})]})},warehouse:Ye,role:Ye,account:Ye,ssh:null!=(Fe=(0,o.a)().get("ssh_tunnel.form.switch"))?Fe:De,project_id:({changeMethods:e,getValidation:a,validationErrors:t,db:n})=>{var l;return(0,Y.Y)(Y.FK,{children:(0,Y.Y)(F.A,{id:"project_id",name:"project_id",required:!0,value:null==n||null==(l=n.parameters)?void 0:l.project_id,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.project_id,placeholder:"your-project-1234-a1",label:(0,d.t)("Project Id"),onChange:e.onParametersChange,helpText:(0,d.t)("Enter the unique project id for your database.")})})}},Ne=({dbModel:e,db:a,editNewDb:t,getPlaceholder:n,getValidation:l,isEditMode:r=!1,onAddTableCatalog:i,onChange:o,onExtraInputChange:s,onEncryptedExtraInputChange:d,onParametersChange:c,onParametersUploadFileChange:h,onQueryChange:u,onRemoveTableCatalog:p,sslForced:m,validationErrors:g,clearValidationErrors:b})=>{const v=null==e?void 0:e.parameters;return(0,Y.Y)(ve.lV,{children:(0,Y.Y)("div",{css:e=>[V,X(e)],children:v&&ke.filter((e=>Object.keys(v.properties).includes(e)||"database_name"===e)).map((e=>{var f,_,y;return $e[e]({required:null==(f=v.required)?void 0:f.includes(e),changeMethods:{onParametersChange:c,onChange:o,onQueryChange:u,onParametersUploadFileChange:h,onAddTableCatalog:i,onRemoveTableCatalog:p,onExtraInputChange:s,onEncryptedExtraInputChange:d},validationErrors:g,getValidation:l,clearValidationErrors:b,db:a,key:e,field:e,default_value:null==(_=v.properties[e])?void 0:_.default,description:null==(y=v.properties[e])?void 0:y.description,isEditMode:r,sslForced:m,editNewDb:t,placeholder:n?n(e):void 0})}))})})},Ee=(0,N.xK)(),Ie=Ee?Ee.support:"https://superset.apache.org/docs/configuration/databases#installing-database-drivers",Te={postgresql:"https://superset.apache.org",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},Ue=({isLoading:e,isEditMode:a,useSqlAlchemyForm:t,hasConnectedDb:n,db:l,dbName:r,dbModel:i,editNewDb:o,fileList:s})=>{const c=s&&(null==s?void 0:s.length)>0,h=(0,Y.FD)(H,{children:[(0,Y.Y)(ie,{children:null==l?void 0:l.backend}),(0,Y.Y)(oe,{children:r})]}),u=(0,Y.FD)(H,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,Y.Y)("h4",{children:(0,d.t)("Enter Primary Credentials")}),(0,Y.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn how to connect your database")," ",(0,Y.Y)("a",{href:(null==Ee?void 0:Ee.default)||Ie,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})]}),p=(0,Y.Y)(he,{children:(0,Y.FD)(H,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:3,stepLast:3})}),(0,Y.Y)("h4",{className:"step-3-text",children:(0,d.t)("Database connected")}),(0,Y.Y)("p",{className:"subheader-text",children:(0,d.t)("Create a dataset to begin visualizing your data as a chart or go to\n          SQL Lab to query your data.")})]})}),m=(0,Y.Y)(he,{children:(0,Y.FD)(H,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:3})}),(0,Y.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})}),(0,Y.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn more about")," ",(0,Y.FD)("a",{href:(g=null==l?void 0:l.engine,g?Ee?Ee[g]||Ee.default:Te[g]?Te[g]:`https://superset.apache.org/docs/databases/${g}`:null),target:"_blank",rel:"noopener noreferrer",children:[(0,d.t)("connecting to %(dbModelName)s",{dbModelName:i.name}),"."]})]})]})});var g;const b=(0,Y.Y)(H,{children:(0,Y.FD)("div",{className:"select-db",children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:1,stepLast:3})}),(0,Y.Y)("h4",{children:(0,d.t)("Select a database to connect")})]})}),v=(0,Y.Y)(he,{children:(0,Y.FD)(H,{children:[(0,Y.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,Y.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})}),(0,Y.Y)("p",{className:"helper-bottom",children:c?s[0].name:""})]})});return c?v:e?(0,Y.Y)(Y.FK,{}):a?h:t?u:n&&!o?p:l||o?m:b};var qe=t(78697),Pe=t(36255),Oe=t(27236);const Le=s.I4.div`
  padding-top: ${({theme:e})=>2*e.gridUnit}px;
  label {
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,Me=(0,s.I4)(g.fI)`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
`,He=(0,s.I4)(g.Wq.Item)`
  margin-bottom: 0 !important;
`,Re=(0,s.I4)(Pe.A.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,ze=({db:e,onSSHTunnelParametersChange:a,setSSHTunnelLoginMethod:t})=>{var n,l,r,i,o,s;const[c,u]=(0,h.useState)(Ge.Password);return(0,Y.FD)(ve.lV,{children:[(0,Y.FD)(Me,{gutter:16,children:[(0,Y.Y)(g.fv,{xs:24,md:12,children:(0,Y.FD)(Le,{children:[(0,Y.Y)(ve.lR,{htmlFor:"server_address",required:!0,children:(0,d.t)("SSH Host")}),(0,Y.Y)(_e.pd,{name:"server_address",type:"text",placeholder:(0,d.t)("e.g. 127.0.0.1"),value:(null==e||null==(n=e.ssh_tunnel)?void 0:n.server_address)||"",onChange:a,"data-test":"ssh-tunnel-server_address-input"})]})}),(0,Y.Y)(g.fv,{xs:24,md:12,children:(0,Y.FD)(Le,{children:[(0,Y.Y)(ve.lR,{htmlFor:"server_port",required:!0,children:(0,d.t)("SSH Port")}),(0,Y.Y)(_e.pd,{name:"server_port",placeholder:(0,d.t)("22"),type:"number",value:null==e||null==(l=e.ssh_tunnel)?void 0:l.server_port,onChange:a,"data-test":"ssh-tunnel-server_port-input"})]})})]}),(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(Le,{children:[(0,Y.Y)(ve.lR,{htmlFor:"username",required:!0,children:(0,d.t)("Username")}),(0,Y.Y)(_e.pd,{name:"username",type:"text",placeholder:(0,d.t)("e.g. Analytics"),value:(null==e||null==(r=e.ssh_tunnel)?void 0:r.username)||"",onChange:a,"data-test":"ssh-tunnel-username-input"})]})})}),(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(Le,{children:[(0,Y.Y)(ve.lR,{htmlFor:"use_password",required:!0,children:(0,d.t)("Login with")}),(0,Y.Y)(He,{name:"use_password",initialValue:c,children:(0,Y.FD)(qe.s.Group,{onChange:({target:{value:e}})=>{u(e),t(e)},children:[(0,Y.Y)(qe.s,{value:Ge.Password,"data-test":"ssh-tunnel-use_password-radio",children:(0,d.t)("Password")}),(0,Y.Y)(qe.s,{value:Ge.PrivateKey,"data-test":"ssh-tunnel-use_private_key-radio",children:(0,d.t)("Private Key & Password")})]})})]})})}),c===Ge.Password&&(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(Le,{children:[(0,Y.Y)(ve.lR,{htmlFor:"password",required:!0,children:(0,d.t)("SSH Password")}),(0,Y.Y)(Re,{name:"password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(i=e.ssh_tunnel)?void 0:i.password)||"",onChange:a,"data-test":"ssh-tunnel-password-input",iconRender:e=>e?(0,Y.Y)(Oe.A,{title:"Hide password.",children:(0,Y.Y)(x.F.EyeInvisibleOutlined,{})}):(0,Y.Y)(Oe.A,{title:"Show password.",children:(0,Y.Y)(x.F.EyeOutlined,{})}),role:"textbox"})]})})}),c===Ge.PrivateKey&&(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(Le,{children:[(0,Y.Y)(ve.lR,{htmlFor:"private_key",required:!0,children:(0,d.t)("Private Key")}),(0,Y.Y)(_e.fs,{name:"private_key",placeholder:(0,d.t)("Paste Private Key here"),value:(null==e||null==(o=e.ssh_tunnel)?void 0:o.private_key)||"",onChange:a,"data-test":"ssh-tunnel-private_key-input",rows:4})]})})}),(0,Y.Y)(Me,{gutter:16,children:(0,Y.Y)(g.fv,{xs:24,children:(0,Y.FD)(Le,{children:[(0,Y.Y)(ve.lR,{htmlFor:"private_key_password",required:!0,children:(0,d.t)("Private Key Password")}),(0,Y.Y)(Re,{name:"private_key_password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(s=e.ssh_tunnel)?void 0:s.private_key_password)||"",onChange:a,"data-test":"ssh-tunnel-private_key_password-input",iconRender:e=>e?(0,Y.Y)(Oe.A,{title:"Hide password.",children:(0,Y.Y)(x.F.EyeInvisibleOutlined,{})}):(0,Y.Y)(Oe.A,{title:"Show password.",children:(0,Y.Y)(x.F.EyeOutlined,{})}),role:"textbox"})]})})})]})]})},je=(0,o.a)(),Be=JSON.stringify({allows_virtual_table_explore:!0}),Ve={[S.GSheet]:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},Ke=(0,s.I4)(m.Ay)`
  .ant-tabs-content {
    display: flex;
    width: 100%;
    overflow: inherit;

    & > .ant-tabs-tabpane {
      position: relative;
    }
  }
`,We=s.I4.div`
  ${({theme:e})=>`\n    margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;\n  `};
`,Qe=s.I4.div`
  ${({theme:e})=>`\n    padding: 0px ${4*e.gridUnit}px;\n  `};
`;var Je,Ge;!function(e){e[e.AddTableCatalogSheet=0]="AddTableCatalogSheet",e[e.ConfigMethodChange=1]="ConfigMethodChange",e[e.DbSelected=2]="DbSelected",e[e.EditorChange=3]="EditorChange",e[e.ExtraEditorChange=4]="ExtraEditorChange",e[e.ExtraInputChange=5]="ExtraInputChange",e[e.EncryptedExtraInputChange=6]="EncryptedExtraInputChange",e[e.Fetched=7]="Fetched",e[e.InputChange=8]="InputChange",e[e.ParametersChange=9]="ParametersChange",e[e.QueryChange=10]="QueryChange",e[e.RemoveTableCatalogSheet=11]="RemoveTableCatalogSheet",e[e.Reset=12]="Reset",e[e.TextChange=13]="TextChange",e[e.ParametersSSHTunnelChange=14]="ParametersSSHTunnelChange",e[e.SetSSHTunnelLoginMethod=15]="SetSSHTunnelLoginMethod",e[e.RemoveSSHTunnelConfig=16]="RemoveSSHTunnelConfig"}(Je||(Je={})),function(e){e[e.Password=0]="Password",e[e.PrivateKey=1]="PrivateKey"}(Ge||(Ge={}));const Xe=s.I4.div`
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  margin-left: ${({theme:e})=>3*e.gridUnit}px;
`;function Ze(e,a){var t,n,r,i;const o={...e||{}};let s,d,c={},h="";const u=JSON.parse(o.extra||"{}");switch(a.type){case Je.ExtraEditorChange:try{d=JSON.parse(a.payload.json||"{}")}catch(e){d=a.payload.json}return{...o,extra:JSON.stringify({...u,[a.payload.name]:d})};case Je.EncryptedExtraInputChange:return{...o,masked_encrypted_extra:JSON.stringify({...JSON.parse(o.masked_encrypted_extra||"{}"),[a.payload.name]:a.payload.value})};case Je.ExtraInputChange:return"schema_cache_timeout"===a.payload.name||"table_cache_timeout"===a.payload.name?{...o,extra:JSON.stringify({...u,metadata_cache_timeout:{...null==u?void 0:u.metadata_cache_timeout,[a.payload.name]:a.payload.value}})}:"schemas_allowed_for_file_upload"===a.payload.name?{...o,extra:JSON.stringify({...u,schemas_allowed_for_file_upload:(a.payload.value||"").split(",").filter((e=>""!==e))})}:"http_path"===a.payload.name?{...o,extra:JSON.stringify({...u,engine_params:{connect_args:{[a.payload.name]:null==(p=a.payload.value)?void 0:p.trim()}}})}:"expand_rows"===a.payload.name?{...o,extra:JSON.stringify({...u,schema_options:{...null==u?void 0:u.schema_options,[a.payload.name]:!!a.payload.value}})}:{...o,extra:JSON.stringify({...u,[a.payload.name]:"checkbox"===a.payload.type?a.payload.checked:a.payload.value})};var p;case Je.InputChange:return"checkbox"===a.payload.type?{...o,[a.payload.name]:a.payload.checked}:{...o,[a.payload.name]:a.payload.value};case Je.ParametersChange:if(null!=(t=a.payload.type)&&t.startsWith("catalog")&&void 0!==o.catalog){var m;const e=[...o.catalog],t=null==(m=a.payload.type)?void 0:m.split("-")[1],n=e[parseInt(t,10)]||{};return void 0!==a.payload.value&&(n[a.payload.name]=a.payload.value),e.splice(parseInt(t,10),1,n),s=e.reduce(((e,a)=>{const t={...e};return t[a.name]=a.value,t}),{}),{...o,catalog:e,parameters:{...o.parameters,catalog:s}}}return{...o,parameters:{...o.parameters,[a.payload.name]:a.payload.value}};case Je.ParametersSSHTunnelChange:return{...o,ssh_tunnel:{...o.ssh_tunnel,[a.payload.name]:a.payload.value}};case Je.SetSSHTunnelLoginMethod:{let e={};var g,b,v;return null!=o&&o.ssh_tunnel&&(e=l()(o.ssh_tunnel,["id","server_address","server_port","username"])),a.payload.login_method===Ge.PrivateKey?{...o,ssh_tunnel:{private_key:null==o||null==(g=o.ssh_tunnel)?void 0:g.private_key,private_key_password:null==o||null==(b=o.ssh_tunnel)?void 0:b.private_key_password,...e}}:a.payload.login_method===Ge.Password?{...o,ssh_tunnel:{password:null==o||null==(v=o.ssh_tunnel)?void 0:v.password,...e}}:{...o}}case Je.RemoveSSHTunnelConfig:return{...o,ssh_tunnel:void 0};case Je.AddTableCatalogSheet:return void 0!==o.catalog?{...o,catalog:[...o.catalog,{name:"",value:""}]}:{...o,catalog:[{name:"",value:""}]};case Je.RemoveTableCatalogSheet:return null==(n=o.catalog)||n.splice(a.payload.indexToDelete,1),{...o};case Je.EditorChange:return{...o,[a.payload.name]:a.payload.json};case Je.QueryChange:return{...o,parameters:{...o.parameters,query:Object.fromEntries(new URLSearchParams(a.payload.value))},query_input:a.payload.value};case Je.TextChange:return{...o,[a.payload.name]:a.payload.value};case Je.Fetched:if(c=(null==(r=a.payload)||null==(i=r.parameters)?void 0:i.query)||{},h=Object.entries(c).map((([e,a])=>`${e}=${a}`)).join("&"),a.payload.masked_encrypted_extra&&a.payload.configuration_method===C.DynamicForm){var f;const e=null==(f={...JSON.parse(a.payload.extra||"{}")}.engine_params)?void 0:f.catalog,t=Object.entries(e||{}).map((([e,a])=>({name:e,value:a})));return{...a.payload,engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,catalog:t,parameters:{...a.payload.parameters||o.parameters,catalog:e},query_input:h}}return{...a.payload,masked_encrypted_extra:a.payload.masked_encrypted_extra||"",engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,parameters:a.payload.parameters||o.parameters,ssh_tunnel:a.payload.ssh_tunnel||o.ssh_tunnel,query_input:h};case Je.DbSelected:return{...a.payload,extra:Be,expose_in_sqllab:!0};case Je.ConfigMethodChange:return{...a.payload};case Je.Reset:default:return null}}const ea=(0,D.Ay)((({addDangerToast:e,addSuccessToast:a,onDatabaseAdd:t,onHide:n,show:l,databaseId:r,dbEngine:o})=>{var _,y,D,T;const U=(0,s.DP)(),[q,P]=(0,h.useReducer)(Ze,null),{state:{loading:O,resource:L,error:M},fetchResource:H,createResource:B,updateResource:X,clearError:Z}=(0,N.fn)("database",(0,d.t)("database"),e,"connection"),[ee,ae]=(0,h.useState)("1"),[ie,oe]=(0,N.d5)(),[se,ue,ge]=(0,N.Y8)(),[ve,fe]=(0,h.useState)(!1),[_e,ye]=(0,h.useState)(!1),[xe,Ye]=(0,h.useState)(""),[we,Ce]=(0,h.useState)(!1),[Se,Ae]=(0,h.useState)(!1),[Fe,ke]=(0,h.useState)(!1),[$e,Ee]=(0,h.useState)({}),[Te,qe]=(0,h.useState)({}),[Pe,Oe]=(0,h.useState)({}),[Le,Me]=(0,h.useState)({}),[He,Re]=(0,h.useState)(!1),[Be,Ge]=(0,h.useState)([]),[ea,aa]=(0,h.useState)(!1),[ta,na]=(0,h.useState)(),[la,ra]=(0,h.useState)([]),[ia,oa]=(0,h.useState)([]),[sa,da]=(0,h.useState)([]),[ca,ha]=(0,h.useState)([]),[ua,pa]=(0,h.useState)({}),ma=null!=(_=je.get("ssh_tunnel.form.switch"))?_:De,[ga,ba]=(0,h.useState)(void 0);let va=je.get("databaseconnection.extraOption");va&&(va={...va,onEdit:e=>{pa({...ua,...e})}});const fa=(0,E.B)(),_a=(0,N.g9)(),ya=(0,N.Fp)(),xa=!!r,Ya=ya||!(null==q||!q.engine||!Ve[q.engine]),wa=(null==q?void 0:q.configuration_method)===C.SqlalchemyUri,Ca=xa||wa,Sa=se||M,Aa=(0,u.W6)(),Da=(null==ie||null==(y=ie.databases)?void 0:y.find((e=>e.engine===(xa?null==q?void 0:q.backend:null==q?void 0:q.engine)&&e.default_driver===(null==q?void 0:q.driver))))||(null==ie||null==(D=ie.databases)?void 0:D.find((e=>e.engine===(xa?null==q?void 0:q.backend:null==q?void 0:q.engine))))||{},Fa=e=>{if("database"===e)return(0,d.t)("e.g. world_population")},ka=(0,h.useCallback)(((e,a)=>{P({type:e,payload:a})}),[]),$a=(0,h.useCallback)((()=>{ge(null)}),[ge]),Na=(0,h.useCallback)((({target:e})=>{ka(Je.ParametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})}),[ka]),Ea=()=>{P({type:Je.Reset}),fe(!1),$a(),Z(),Ce(!1),Ge([]),aa(!1),na(""),ra([]),oa([]),da([]),ha([]),Ee({}),qe({}),Oe({}),Me({}),Re(!1),ba(void 0),n()},Ia=e=>{Aa.push(e)},{state:{alreadyExists:Ta,passwordsNeeded:Ua,sshPasswordNeeded:qa,sshPrivateKeyNeeded:Pa,sshPrivateKeyPasswordNeeded:Oa,loading:La,failed:Ma},importResource:Ha}=(0,N.bN)("database",(0,d.t)("database"),(e=>{na(e)})),Ra=async()=>{var n,l;let r;if(Ae(!0),null==(n=va)||n.onSave(ua,q).then((({error:a})=>{a&&(r=a,e(a))})),r)return void Ae(!1);const o={...q||{}};if(o.configuration_method===C.DynamicForm){var s,c;null!=o&&null!=(s=o.parameters)&&s.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}}));const a=await ue(o,!0);if(!i()(se)||null!=a&&a.length)return e((0,d.t)("Connection failed, please check your connection settings.")),void Ae(!1);const t=xa?null==(c=o.parameters_schema)?void 0:c.properties:null==Da?void 0:Da.parameters.properties,n=JSON.parse(o.masked_encrypted_extra||"{}");Object.keys(t||{}).forEach((e=>{var a,l,r,i;t[e]["x-encrypted-extra"]&&null!=(a=o.parameters)&&a[e]&&("object"==typeof(null==(l=o.parameters)?void 0:l[e])?(n[e]=null==(r=o.parameters)?void 0:r[e],o.parameters[e]=JSON.stringify(o.parameters[e])):n[e]=JSON.parse((null==(i=o.parameters)?void 0:i[e])||"{}"))})),o.masked_encrypted_extra=JSON.stringify(n),o.engine===S.GSheet&&(o.impersonate_user=!0)}if(null!=o&&null!=(l=o.parameters)&&l.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}})),!1===ga&&(o.ssh_tunnel=null),null!=q&&q.id){if(await X(q.id,o,o.configuration_method===C.DynamicForm)){var h;if(t&&t(),null==(h=va)||h.onSave(ua,q).then((({error:a})=>{a&&(r=a,e(a))})),r)return void Ae(!1);we||(Ea(),a((0,d.t)("Database settings updated")))}}else if(q){if(await B(o,o.configuration_method===C.DynamicForm)){var u;if(fe(!0),t&&t(),null==(u=va)||u.onSave(ua,q).then((({error:a})=>{a&&(r=a,e(a))})),r)return void Ae(!1);Ca&&(Ea(),a((0,d.t)("Database connected")))}}else{if(aa(!0),!(Be[0].originFileObj instanceof File))return;await Ha(Be[0].originFileObj,$e,Te,Pe,Le,He)&&(t&&t(),Ea(),a((0,d.t)("Database connected")))}ye(!0),Ce(!1),Ae(!1)},za=e=>{if("Other"===e)P({type:Je.DbSelected,payload:{database_name:e,configuration_method:C.SqlalchemyUri,engine:void 0,engine_information:{supports_file_upload:!0}}});else{const a=null==ie?void 0:ie.databases.filter((a=>a.name===e))[0],{engine:t,parameters:n,engine_information:l,default_driver:r,sqlalchemy_uri_placeholder:i}=a,o=void 0!==n;P({type:Je.DbSelected,payload:{database_name:e,engine:t,configuration_method:o?C.DynamicForm:C.SqlalchemyUri,engine_information:l,driver:r,sqlalchemy_uri_placeholder:i}}),t===S.GSheet&&P({type:Je.AddTableCatalogSheet})}},ja=()=>{L&&H(L.id),ye(!1),Ce(!0)},Ba=()=>{we&&fe(!1),ea&&aa(!1),Ma&&(aa(!1),na(""),ra([]),oa([]),da([]),ha([]),Ee({}),qe({}),Oe({}),Me({})),P({type:Je.Reset}),Ge([])},Va=()=>q?!ve||we?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:Ba,children:(0,d.t)("Back")},"back"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,loading:Se,children:(0,d.t)("Connect")},"submit")]}):(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:ja,children:(0,d.t)("Back")},"back"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,"data-test":"modal-confirm-button",loading:Se,children:(0,d.t)("Finish")},"submit")]}):ea?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:Ba,children:(0,d.t)("Back")},"back"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,disabled:!!(La||Ta.length&&!He||Ua.length&&"{}"===JSON.stringify($e)||qa.length&&"{}"===JSON.stringify(Te)||Pa.length&&"{}"===JSON.stringify(Pe)||Oa.length&&"{}"===JSON.stringify(Le)),loading:Se,children:(0,d.t)("Connect")},"submit")]}):(0,Y.Y)(Y.FK,{}),Ka=(0,h.useRef)(!0);(0,h.useEffect)((()=>{Ka.current?Ka.current=!1:La||Ta.length||Ua.length||qa.length||Pa.length||Oa.length||Se||Ma||(Ea(),a((0,d.t)("Database connected")))}),[Ta,Ua,La,Ma,qa,Pa,Oa]),(0,h.useEffect)((()=>{l&&(ae("1"),Ae(!0),oe()),r&&l&&xa&&r&&(O||H(r).catch((a=>e((0,d.t)("Sorry there was an error fetching database information: %s",a.message)))))}),[l,r]),(0,h.useEffect)((()=>{L&&(P({type:Je.Fetched,payload:L}),Ye(L.database_name))}),[L]),(0,h.useEffect)((()=>{Se&&Ae(!1),ie&&o&&za(o)}),[ie]),(0,h.useEffect)((()=>{var e;ea&&(null==(e=document)||e.getElementsByClassName("ant-upload-list-item-name")[0].scrollIntoView())}),[ea]),(0,h.useEffect)((()=>{ra([...Ua])}),[Ua]),(0,h.useEffect)((()=>{oa([...qa])}),[qa]),(0,h.useEffect)((()=>{da([...Pa])}),[Pa]),(0,h.useEffect)((()=>{ha([...Oa])}),[Oa]),(0,h.useEffect)((()=>{var e;void 0!==(null==q||null==(e=q.parameters)?void 0:e.ssh)&&ba(q.parameters.ssh)}),[null==q||null==(T=q.parameters)?void 0:T.ssh]);const Wa=()=>ta?(0,Y.Y)(Q,{children:(0,Y.Y)($.A,{errorMessage:ta,showDbInstallInstructions:la.length>0})}):null,Qa=e=>{var a,t;const n=null!=(a=null==(t=e.currentTarget)?void 0:t.value)?a:"";Re(n.toUpperCase()===(0,d.t)("OVERWRITE"))},Ja=()=>{let e=[];var a;return i()(M)?i()(se)||"GENERIC_DB_ENGINE_ERROR"!==(null==se?void 0:se.error_type)||(e=[(null==se?void 0:se.description)||(null==se?void 0:se.message)]):e="object"==typeof M?Object.values(M):"string"==typeof M?[M]:[],e.length?(0,Y.Y)(We,{children:(0,Y.Y)(k.A,{title:(0,d.t)("Database Creation Error"),description:(0,d.t)('We are unable to connect to your database. Click "See more" for database-provided information that may help troubleshoot the issue.'),descriptionDetails:(null==(a=e)?void 0:a[0])||(null==se?void 0:se.description)})}):(0,Y.Y)(Y.FK,{})},Ga=()=>{Ae(!0),H(null==L?void 0:L.id).then((e=>{(0,p.SO)(p.Hh.Database,e)}))},Xa=()=>(0,Y.Y)(ze,{db:q,onSSHTunnelParametersChange:({target:e})=>{ka(Je.ParametersSSHTunnelChange,{type:e.type,name:e.name,value:e.value}),$a()},setSSHTunnelLoginMethod:e=>P({type:Je.SetSSHTunnelLoginMethod,payload:{login_method:e}})}),Za=()=>(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ne,{isEditMode:xa,db:q,sslForced:!1,dbModel:Da,onAddTableCatalog:()=>{P({type:Je.AddTableCatalogSheet})},onQueryChange:({target:e})=>ka(Je.QueryChange,{name:e.name,value:e.value}),onExtraInputChange:({target:e})=>ka(Je.ExtraInputChange,{name:e.name,value:e.value}),onEncryptedExtraInputChange:({target:e})=>ka(Je.EncryptedExtraInputChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{P({type:Je.RemoveTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:Na,onChange:({target:e})=>ka(Je.TextChange,{name:e.name,value:e.value}),getValidation:()=>ue(q),validationErrors:se,getPlaceholder:Fa,clearValidationErrors:$a}),ga&&(0,Y.Y)(Qe,{children:Xa()})]});if(Be.length>0&&(Ta.length||la.length||ia.length||sa.length||ca.length))return(0,Y.FD)(v.Ay,{centered:!0,css:e=>[z,K(e),J(e),G(e)],footer:Va(),maskClosable:!1,name:"database",onHide:Ea,onHandledPrimaryAction:Ra,primaryButtonName:(0,d.t)("Connect"),show:l,title:(0,Y.Y)("h4",{children:(0,d.t)("Connect a database")}),width:"500px",children:[(0,Y.Y)(Ue,{db:q,dbName:xe,dbModel:Da,fileList:Be,hasConnectedDb:ve,isEditMode:xa,isLoading:Se,useSqlAlchemyForm:wa}),Ta.length?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Q,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>(e=>c.AH`
  margin: ${4*e.gridUnit}px 0;

  .antd5-alert-message {
    margin: 0;
  }
`)(e),type:"warning",showIcon:!0,message:"",description:(0,d.t)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?")})}),(0,Y.Y)(F.A,{id:"confirm_overwrite",name:"confirm_overwrite",required:!0,validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.confirm_overwrite,label:(0,d.t)('Type "%s" to confirm',(0,d.t)("OVERWRITE")),onChange:Qa,css:V})]}):null,Wa(),la.length||ia.length||sa.length||ca.length?[...new Set([...la,...ia,...sa,...ca])].map((e=>(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Q,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>W(e),type:"info",showIcon:!0,message:"Database passwords",description:(0,d.t)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in explore files and should be added manually after the import if they are needed.')})}),(null==la?void 0:la.indexOf(e))>=0&&(0,Y.Y)(F.A,{id:"password_needed",name:"password_needed",required:!0,value:$e[e],onChange:a=>Ee({...$e,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.password_needed,label:(0,d.t)("%s PASSWORD",e.slice(10)),css:V}),(null==ia?void 0:ia.indexOf(e))>=0&&(0,Y.Y)(F.A,{id:"ssh_tunnel_password_needed",name:"ssh_tunnel_password_needed",required:!0,value:Te[e],onChange:a=>qe({...Te,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.ssh_tunnel_password_needed,label:(0,d.t)("%s SSH TUNNEL PASSWORD",e.slice(10)),css:V}),(null==sa?void 0:sa.indexOf(e))>=0&&(0,Y.Y)(F.A,{id:"ssh_tunnel_private_key_needed",name:"ssh_tunnel_private_key_needed",required:!0,value:Pe[e],onChange:a=>Oe({...Pe,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.ssh_tunnel_private_key_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY",e.slice(10)),css:V}),(null==ca?void 0:ca.indexOf(e))>=0&&(0,Y.Y)(F.A,{id:"ssh_tunnel_private_key_password_needed",name:"ssh_tunnel_private_key_password_needed",required:!0,value:Le[e],onChange:a=>Me({...Le,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==se?void 0:se.ssh_tunnel_private_key_password_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY PASSWORD",e.slice(10)),css:V})]}))):null]});const et=xa?(e=>(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(ce,{onClick:Ea,children:(0,d.t)("Close")},"close"),(0,Y.Y)(ce,{buttonStyle:"primary",onClick:Ra,disabled:null==e?void 0:e.is_managed_externally,loading:Se,tooltip:null!=e&&e.is_managed_externally?(0,d.t)("This database is managed externally, and can't be edited in Superset"):"",children:(0,d.t)("Finish")},"submit")]}))(q):Va();return Ca?(0,Y.FD)(v.Ay,{css:e=>[R,z,K(e),J(e),G(e)],name:"database","data-test":"database-modal",onHandledPrimaryAction:Ra,onHide:Ea,primaryButtonName:xa?(0,d.t)("Save"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,Y.FD)("h4",{children:[xa?(0,Y.Y)(x.F.EditOutlined,{iconSize:"l",css:c.AH`
                margin: auto ${2*U.gridUnit}px auto 0;
              `}):(0,Y.Y)(x.F.InsertRowAboveOutlined,{iconSize:"l",css:c.AH`
                margin: auto ${2*U.gridUnit}px auto 0;
              `}),xa?(0,d.t)("Edit database"):(0,d.t)("Connect a database")]}),footer:et,maskClosable:!1,children:[(0,Y.Y)(he,{children:(0,Y.Y)(re,{children:(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:q,dbName:xe,dbModel:Da})})}),(0,Y.FD)(Ke,{defaultActiveKey:"1",activeKey:ee,onTabClick:e=>ae(e),animated:{inkBar:!0,tabPane:!0},children:[(0,Y.FD)(m.Ay.TabPane,{tab:(0,Y.Y)("span",{children:(0,d.t)("Basic")}),children:[wa?(0,Y.FD)(te,{children:[(0,Y.FD)(be,{db:q,onInputChange:({target:e})=>ka(Je.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:fa,testConnection:()=>{var t;if(null==q||!q.sqlalchemy_uri)return void e((0,d.t)("Please enter a SQLAlchemy URI to test"));const n={sqlalchemy_uri:(null==q?void 0:q.sqlalchemy_uri)||"",database_name:(null==q||null==(t=q.database_name)?void 0:t.trim())||void 0,impersonate_user:(null==q?void 0:q.impersonate_user)||void 0,extra:null==q?void 0:q.extra,masked_encrypted_extra:(null==q?void 0:q.masked_encrypted_extra)||"",server_cert:(null==q?void 0:q.server_cert)||void 0,ssh_tunnel:!i()(null==q?void 0:q.ssh_tunnel)&&ga?{...q.ssh_tunnel,server_port:Number(q.ssh_tunnel.server_port)}:void 0};ke(!0),(0,N.ym)(n,(a=>{ke(!1),e(a)}),(e=>{ke(!1),a(e)}))},testInProgress:Fe,children:[(0,Y.Y)(ma,{dbModel:Da,db:q,changeMethods:{onParametersChange:Na},clearValidationErrors:$a}),ga&&Xa()]}),(lt=(null==q?void 0:q.backend)||(null==q?void 0:q.engine),void 0!==(null==ie||null==(rt=ie.databases)||null==(it=rt.find((e=>e.backend===lt||e.engine===lt)))?void 0:it.parameters)&&!xa&&(0,Y.FD)("div",{css:e=>j(e),children:[(0,Y.Y)(f.A,{buttonStyle:"link",onClick:()=>P({type:Je.ConfigMethodChange,payload:{database_name:null==q?void 0:q.database_name,configuration_method:C.DynamicForm,engine:null==q?void 0:q.engine}}),css:e=>(e=>c.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`)(e),children:(0,d.t)("Connect this database using the dynamic form instead")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})]}))]}):Za(),!xa&&(0,Y.Y)(Q,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>W(e),message:(0,d.t)("Additional fields may be required"),showIcon:!0,description:(0,Y.FD)(Y.FK,{children:[(0,d.t)("Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has "),(0,Y.Y)("a",{href:Ie,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,d.t)("here")}),"."]}),type:"info"})}),Sa&&Ja()]},"1"),(0,Y.Y)(m.Ay.TabPane,{tab:(0,Y.Y)("span",{children:(0,d.t)("Advanced")}),children:(0,Y.Y)(me,{extraExtension:va,db:q,onInputChange:({target:e})=>ka(Je.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>ka(Je.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>ka(Je.EditorChange,e),onExtraInputChange:({target:e})=>{ka(Je.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{ka(Je.ExtraEditorChange,e)}})},"2")]})]}):(0,Y.FD)(v.Ay,{css:e=>[z,K(e),J(e),G(e)],name:"database",onHandledPrimaryAction:Ra,onHide:Ea,primaryButtonName:ve?(0,d.t)("Finish"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,Y.FD)("h4",{children:[(0,Y.Y)(x.F.InsertRowAboveOutlined,{iconSize:"l",css:c.AH`
              margin: auto ${2*U.gridUnit}px auto 0;
            `}),(0,d.t)("Connect a database")]}),footer:Va(),maskClosable:!1,children:[!Se&&ve?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:q,dbName:xe,dbModel:Da,editNewDb:we}),_e&&(0,Y.FD)(Xe,{children:[(0,Y.Y)(f.A,{buttonStyle:"secondary",onClick:()=>{Ae(!0),Ga(),Ia("/dataset/add/")},children:(0,d.t)("CREATE DATASET")}),(0,Y.Y)(f.A,{buttonStyle:"secondary",onClick:()=>{Ae(!0),Ga(),Ia("/sqllab?db=true")},children:(0,d.t)("QUERY DATA IN SQL LAB")})]}),we?Za():(0,Y.Y)(me,{extraExtension:va,db:q,onInputChange:({target:e})=>ka(Je.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>ka(Je.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>ka(Je.EditorChange,e),onExtraInputChange:({target:e})=>{ka(Je.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>ka(Je.ExtraEditorChange,e)})]}):(0,Y.Y)(Y.FK,{children:!Se&&(q?(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:q,dbName:xe,dbModel:Da}),Ya&&(()=>{var e,a,t,n,l;const{hostname:r}=window.location;let i=(null==ya||null==(e=ya.REGIONAL_IPS)?void 0:e.default)||"";const o=(null==ya?void 0:ya.REGIONAL_IPS)||{};return Object.entries(o).forEach((([e,a])=>{const t=new RegExp(e);r.match(t)&&(i=a)})),(null==q?void 0:q.engine)&&(0,Y.Y)(Q,{children:(0,Y.Y)(b.A,{closable:!1,css:e=>W(e),type:"info",showIcon:!0,message:(null==(a=Ve[q.engine])?void 0:a.message)||(null==ya||null==(t=ya.DEFAULT)?void 0:t.message),description:(null==(n=Ve[q.engine])?void 0:n.description)||(null==ya||null==(l=ya.DEFAULT)?void 0:l.description)+i})})})(),Za(),(0,Y.Y)("div",{css:e=>j(e),children:Da.engine!==S.GSheet&&(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(f.A,{"data-test":"sqla-connect-btn",buttonStyle:"link",onClick:()=>P({type:Je.ConfigMethodChange,payload:{engine:q.engine,configuration_method:C.SqlalchemyUri,database_name:q.database_name}}),css:ne,children:(0,d.t)("Connect this database with a SQLAlchemy URI string instead")}),(0,Y.Y)(A.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"})]})}),Sa&&Ja()]}):(0,Y.FD)(de,{children:[(0,Y.Y)(Ue,{isLoading:Se,isEditMode:xa,useSqlAlchemyForm:wa,hasConnectedDb:ve,db:q,dbName:xe,dbModel:Da}),(0,Y.Y)("div",{className:"preferred",children:null==ie||null==(nt=ie.databases)?void 0:nt.filter((e=>e.preferred)).map((e=>(0,Y.Y)(w,{className:"preferred-item",onClick:()=>za(e.name),buttonText:e.name,icon:null==_a?void 0:_a[e.engine]},`${e.name}`)))}),(0,Y.FD)("div",{className:"available",children:[(0,Y.Y)("h4",{className:"available-label",children:(0,d.t)("Or choose from a list of other databases we support:")}),(0,Y.Y)("div",{className:"control-label",children:(0,d.t)("Supported databases")}),(0,Y.FD)(g._P,{className:"available-select",onChange:za,placeholder:(0,d.t)("Choose a database..."),showSearch:!0,children:[null==(at=[...(null==ie?void 0:ie.databases)||[]])?void 0:at.sort(((e,a)=>e.name.localeCompare(a.name))).map(((e,a)=>(0,Y.Y)(g._P.Option,{value:e.name,children:e.name},`database-${a}`))),(0,Y.Y)(g._P.Option,{value:"Other",children:(0,d.t)("Other")},"Other")]}),(0,Y.Y)(b.A,{showIcon:!0,closable:!1,css:e=>W(e),type:"info",message:(null==ya||null==(tt=ya.ADD_DATABASE)?void 0:tt.message)||(0,d.t)("Want to add a new database?"),description:null!=ya&&ya.ADD_DATABASE?(0,Y.FD)(Y.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. "),(0,Y.Y)("a",{href:null==ya?void 0:ya.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer",children:null==ya?void 0:ya.ADD_DATABASE.contact_description_link})," ",null==ya?void 0:ya.ADD_DATABASE.description]}):(0,Y.FD)(Y.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver "),(0,Y.Y)("a",{href:Ie,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})})]}),(0,Y.Y)(pe,{children:(0,Y.Y)(g._O,{name:"databaseFile",id:"databaseFile","data-test":"database-file-input",accept:".yaml,.json,.yml,.zip",customRequest:()=>{},onChange:async e=>{na(""),ra([]),oa([]),da([]),ha([]),Ee({}),qe({}),Oe({}),Me({}),aa(!0),Ge([{...e.file,status:"done"}]),e.file.originFileObj instanceof File&&await Ha(e.file.originFileObj,$e,Te,Pe,Le,He)&&(null==t||t())},onRemove:e=>(Ge(Be.filter((a=>a.uid!==e.uid))),!1),children:(0,Y.Y)(f.A,{"data-test":"import-database-btn",buttonStyle:"link",type:"link",css:le,children:(0,d.t)("Import database from file")})})}),Wa()]}))}),Se&&(0,Y.Y)(I.A,{})]});var at,tt,nt,lt,rt,it}))},62221:(e,a,t)=>{var n;function l(e,a){try{const t=localStorage.getItem(e);return null===t?a:JSON.parse(t)}catch{return a}}function r(e,a){try{localStorage.setItem(e,JSON.stringify(a))}catch{}}function i(e,a){return l(e,a)}function o(e,a){r(e,a)}t.d(a,{Gq:()=>i,Hh:()=>n,SO:()=>o,SX:()=>l,Wr:()=>r}),function(e){e.Database="db",e.ChartSplitSizes="chart_split_sizes",e.ControlsWidth="controls_width",e.DatasourceWidth="datasource_width",e.IsDatapanelOpen="is_datapanel_open",e.HomepageChartFilter="homepage_chart_filter",e.HomepageDashboardFilter="homepage_dashboard_filter",e.HomepageCollapseState="homepage_collapse_state",e.HomepageActivityFilter="homepage_activity_filter",e.DatasetnameSetSuccessful="datasetname_set_successful",e.SqllabIsAutocompleteEnabled="sqllab__is_autocomplete_enabled",e.SqllabIsRenderHtmlEnabled="sqllab__is_render_html_enabled",e.ExploreDataTableOriginalFormattedTimeColumns="explore__data_table_original_formatted_time_columns",e.DashboardCustomFilterBarWidths="dashboard__custom_filter_bar_widths",e.DashboardExploreContext="dashboard__explore_context",e.DashboardEditorShowOnlyMyCharts="dashboard__editor_show_only_my_charts",e.CommonResizableSidebarWidths="common__resizable_sidebar_widths"}(n||(n={}))},82741:(e,a,t)=>{t.d(a,{A:()=>oe});var n=t(38221),l=t.n(n),r=t(96540),i=t(96453),o=t(17437),s=t(32132),d=t(15595),c=t(6749),h=t(19129),u=t(61574),p=t(71519),m=t(78532),g=t(67073),b=t(35837),v=t(27023),f=t(62193),_=t.n(f),y=t(58156),x=t.n(y),Y=t(58561),w=t.n(Y),C=t(61225),S=t(33231),A=t(72391),D=t(78518),F=t(35742),k=t(35768),$=t(83188),N=t(84666),E=t(65256),I=t(43293),T=t(19980),U=t(30703),q=t(2445);const P=({version:e="unknownVersion",sha:a="unknownSHA",build:t="unknownBuild"})=>{const n=`https://apachesuperset.gateway.scarf.sh/pixel/0d3461e1-abb1-4691-a0aa-5ed50de66af0/${e}/${a}/${t}`;return(0,q.Y)("img",{referrerPolicy:"no-referrer-when-downgrade",src:n,width:0,height:0,alt:""})},{SubMenu:O}=c.NG,L=i.I4.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`,M=i.I4.i`
  margin-top: 2px;
`;function H(e){const{locale:a,languages:t,...n}=e,l=(0,i.DP)();return(0,q.Y)(O,{css:o.AH`
        [data-icon='caret-down'] {
          color: ${l.colors.grayscale.base};
          font-size: ${l.typography.sizes.xxs}px;
          margin-left: ${l.gridUnit}px;
        }
      `,"aria-label":"Languages",title:(0,q.Y)("div",{className:"f16",children:(0,q.Y)(M,{className:`flag ${t[a].flag}`})}),icon:(0,q.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),...n,children:Object.keys(t).map((e=>(0,q.Y)(c.NG.Item,{style:{whiteSpace:"normal",height:"auto"},children:(0,q.FD)(L,{className:"f16",children:[(0,q.Y)("i",{className:`flag ${t[e].flag}`}),(0,q.Y)("a",{href:t[e].url,children:t[e].name})]})},e)))})}var R=t(3139);const z=(0,A.a)(),j=e=>o.AH`
  color: ${e.colors.grayscale.light1};
`,B=i.I4.div`
  display: flex;
  height: 100%;
  flex-direction: row;
  justify-content: ${({align:e})=>e};
  align-items: center;
  margin-right: ${({theme:e})=>e.gridUnit}px;
`,V=i.I4.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`,K=i.I4.a`
  padding-right: ${({theme:e})=>e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`,W=e=>o.AH`
  color: ${e.colors.grayscale.light5};
`,Q=e=>o.AH`
  &:hover {
    color: ${e.colors.primary.base} !important;
    cursor: pointer !important;
  }
`,{SubMenu:J}=c.W1,G=(0,i.I4)(J)`
  ${({theme:e})=>o.AH`
    [data-icon='caret-down'] {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.xxs}px;
      margin-left: ${e.gridUnit}px;
    }
    &.antd5-menu-submenu-active {
      .antd5-menu-title-content {
        color: ${e.colors.primary.base};
      }
    }
  `}
`,X=({align:e,settings:a,navbarRight:t,isFrontendRoute:n,environmentTag:l,setQuery:s})=>{const d=(0,C.d4)((e=>e.user)),u=(0,C.d4)((e=>{var a;return null==(a=e.dashboardInfo)?void 0:a.id})),m=d||{},{roles:b}=m,{CSV_EXTENSIONS:v,COLUMNAR_EXTENSIONS:f,EXCEL_EXTENSIONS:y,ALLOWED_EXTENSIONS:Y,HAS_GSHEETS_INSTALLED:S}=(0,C.d4)((e=>e.common.conf)),[A,O]=(0,r.useState)(!1),[L,M]=(0,r.useState)(!1),[J,X]=(0,r.useState)(!1),[Z,ee]=(0,r.useState)(!1),[ae,te]=(0,r.useState)(""),ne=(0,N.L)("can_sqllab","Superset",b),le=(0,N.L)("can_write","Dashboard",b),re=(0,N.L)("can_write","Chart",b),ie=(0,N.L)("can_write","Database",b),oe=(0,N.L)("can_write","Dataset",b),{canUploadData:se,canUploadCSV:de,canUploadColumnar:ce,canUploadExcel:he}=(0,U.c8)(b,v,f,y,Y),ue=ne||re||le,[pe,me]=(0,r.useState)(!1),[ge,be]=(0,r.useState)(!1),ve=(0,E.N6)(d),fe=pe||ve,_e=[{label:(0,D.t)("Data"),icon:"fa-database",childs:[{label:(0,D.t)("Connect database"),name:R.$.DbConnection,perm:ie&&!ge},{label:(0,D.t)("Create dataset"),name:R.$.DatasetCreation,url:"/dataset/add/",perm:oe&&ge},{label:(0,D.t)("Connect Google Sheet"),name:R.$.GoogleSheets,perm:ie&&S},{label:(0,D.t)("Upload CSV to database"),name:R.$.CSVUpload,perm:de&&fe,disable:ve&&!pe},{label:(0,D.t)("Upload Excel to database"),name:R.$.ExcelUpload,perm:he&&fe,disable:ve&&!pe},{label:(0,D.t)("Upload Columnar file to database"),name:R.$.ColumnarUpload,perm:ce&&fe,disable:ve&&!pe}]},{label:(0,D.t)("SQL query"),url:"/sqllab?new=true",icon:"fa-fw fa-search",perm:"can_sqllab",view:"Superset"},{label:(0,D.t)("Chart"),url:Number.isInteger(u)?`/chart/add?dashboard_id=${u}`:"/chart/add",icon:"fa-fw fa-bar-chart",perm:"can_write",view:"Chart"},{label:(0,D.t)("Dashboard"),url:"/dashboard/new",icon:"fa-fw fa-dashboard",perm:"can_write",view:"Dashboard"}],ye=()=>{F.A.get({endpoint:`/api/v1/database/?q=${w().encode({filters:[{col:"allow_file_upload",opr:"upload_is_enabled",value:!0}]})}`}).then((({json:e})=>{var a;const t=(null==e||null==(a=e.result)?void 0:a.filter((e=>{var a;return null==e||null==(a=e.engine_information)?void 0:a.supports_file_upload})))||[];me((null==t?void 0:t.length)>=1)}))},xe=()=>{F.A.get({endpoint:`/api/v1/database/?q=${w().encode({filters:[{col:"database_name",opr:"neq",value:"examples"}]})}`}).then((({json:e})=>{be(e.count>=1)}))};(0,r.useEffect)((()=>{se&&ye()}),[se]),(0,r.useEffect)((()=>{(ie||oe)&&xe()}),[ie,oe]);const Ye=e=>(0,q.Y)("i",{"data-test":`menu-item-${e.label}`,className:`fa ${e.icon}`}),we=(0,D.t)("Enable 'Allow file uploads to database' in any database's settings"),Ce=e=>e.disable?(0,q.Y)(c.W1.Item,{css:j,disabled:!0,children:(0,q.Y)(h.m_,{placement:"top",title:we,children:e.label})},e.name):(0,q.Y)(c.W1.Item,{css:Q,children:e.url?(0,q.FD)("a",{href:(0,$.A)(e.url),children:[" ",e.label," "]}):e.label},e.name),Se=z.get("navbar.right"),Ae=z.get("navbar.right-menu.item.icon"),De=(0,i.DP)();return(0,q.FD)(B,{align:e,children:[ie&&(0,q.Y)(I.Ay,{onHide:()=>{te(""),O(!1)},show:A,dbEngine:ae,onDatabaseAdd:()=>s({databaseAdded:!0})}),de&&(0,q.Y)(T.A,{onHide:()=>M(!1),show:L,allowedExtensions:v,type:"csv"}),he&&(0,q.Y)(T.A,{onHide:()=>X(!1),show:J,allowedExtensions:y,type:"excel"}),ce&&(0,q.Y)(T.A,{onHide:()=>ee(!1),show:Z,allowedExtensions:f,type:"columnar"}),(null==l?void 0:l.text)&&(0,q.Y)(k.Ay,{css:(0,o.AH)({borderRadius:125*De.gridUnit+"px"},"",""),color:/^#(?:[0-9a-f]{3}){1,2}$/i.test(l.color)?l.color:x()(De.colors,l.color),children:(0,q.Y)("span",{css:W,children:l.text})}),(0,q.FD)(c.W1,{css:o.AH`
          display: flex;
          flex-direction: row;
        `,selectable:!1,mode:"horizontal",onClick:e=>{e.key===R.$.DbConnection?O(!0):e.key===R.$.GoogleSheets?(O(!0),te("Google Sheets")):e.key===R.$.CSVUpload?M(!0):e.key===R.$.ExcelUpload?X(!0):e.key===R.$.ColumnarUpload&&ee(!0)},onOpenChange:e=>(e.length>1&&!_()(null==e?void 0:e.filter((e=>{var a;return e.includes(`sub2_${null==_e||null==(a=_e[0])?void 0:a.label}`)})))&&(se&&ye(),(ie||oe)&&xe()),null),disabledOverflow:!0,children:[Se&&(0,q.Y)(Se,{}),!t.user_is_anonymous&&ue&&(0,q.Y)(G,{"data-test":"new-dropdown",title:(0,q.Y)(g.F.PlusOutlined,{iconColor:De.colors.primary.dark1,"data-test":"new-dropdown-icon"}),icon:(0,q.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),children:null==_e||null==_e.map?void 0:_e.map((e=>{var a;const t=null==(a=e.childs)?void 0:a.some((e=>"object"==typeof e&&!!e.perm));if(e.childs){var l;if(t)return(0,q.Y)(G,{className:"data-menu",title:e.label,icon:Ye(e),children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map(((e,a)=>"string"!=typeof e&&e.name&&e.perm?(0,q.FD)(r.Fragment,{children:[3===a&&(0,q.Y)(c.W1.Divider,{}),Ce(e)]},e.name):null))},`sub2_${e.label}`);if(!e.url)return null}return(0,N.L)(e.perm,e.view,b)&&(0,q.Y)(c.W1.Item,{children:n(e.url)?(0,q.FD)(p.N_,{to:e.url||"",children:[(0,q.Y)("i",{"data-test":`menu-item-${e.label}`,className:`fa ${e.icon}`})," ",e.label]}):(0,q.FD)("a",{href:(0,$.A)(e.url||""),children:[(0,q.Y)("i",{"data-test":`menu-item-${e.label}`,className:`fa ${e.icon}`})," ",e.label]})},e.label)}))},"sub1"),(0,q.FD)(G,{title:(0,D.t)("Settings"),icon:(0,q.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),children:[null==a||null==a.map?void 0:a.map(((e,t)=>{var l;return[(0,q.Y)(c.W1.ItemGroup,{title:e.label,children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map((e=>{if("string"!=typeof e){const a=Ae?(0,q.FD)(V,{children:[e.label,(0,q.Y)(Ae,{menuChild:e})]}):e.label;return(0,q.Y)(c.W1.Item,{children:n(e.url)?(0,q.Y)(p.N_,{to:e.url||"",children:a}):(0,q.Y)("a",{href:e.url||"",children:a})},`${e.label}`)}return null}))},`${e.label}`),t<a.length-1&&(0,q.Y)(c.W1.Divider,{},`divider_${t}`)]})),!t.user_is_anonymous&&[(0,q.Y)(c.W1.Divider,{},"user-divider"),(0,q.FD)(c.W1.ItemGroup,{title:(0,D.t)("User"),children:[t.user_info_url&&(0,q.Y)(c.W1.Item,{children:(0,q.Y)("a",{href:t.user_info_url,children:(0,D.t)("Info")})},"info"),(0,q.Y)(c.W1.Item,{onClick:()=>{localStorage.removeItem("redux")},children:(0,q.Y)("a",{href:t.user_logout_url,children:(0,D.t)("Logout")})},"logout")]},"user-section")],!1]},"sub3_settings"),t.show_language_picker&&(0,q.Y)(H,{locale:t.locale,languages:t.languages})]}),t.documentation_url&&(0,q.FD)(q.FK,{children:[(0,q.Y)(K,{href:t.documentation_url,target:"_blank",rel:"noreferrer",title:t.documentation_text||(0,D.t)("Documentation"),children:t.documentation_icon?(0,q.Y)("i",{className:t.documentation_icon}):(0,q.Y)("i",{className:"fa fa-question"})}),(0,q.Y)("span",{children:" "})]}),t.bug_report_url&&(0,q.FD)(q.FK,{children:[(0,q.Y)(K,{href:t.bug_report_url,target:"_blank",rel:"noreferrer",title:t.bug_report_text||(0,D.t)("Report a bug"),children:t.bug_report_icon?(0,q.Y)("i",{className:t.bug_report_icon}):(0,q.Y)("i",{className:"fa fa-bug"})}),(0,q.Y)("span",{children:" "})]}),t.user_is_anonymous&&(0,q.FD)(K,{href:t.user_login_url,children:[(0,q.Y)("i",{className:"fa fa-fw fa-sign-in"}),(0,D.t)("Login")]}),(0,q.Y)(P,{version:t.version_string,sha:t.version_sha,build:t.build_number})]})},Z=e=>{const[,a]=(0,S.sq)({databaseAdded:S.sJ,datasetAdded:S.sJ});return(0,q.Y)(X,{setQuery:a,...e})};class ee extends r.PureComponent{constructor(...e){super(...e),this.state={hasError:!1},this.noop=()=>{}}static getDerivedStateFromError(){return{hasError:!0}}render(){return this.state.hasError?(0,q.Y)(X,{setQuery:this.noop,...this.props}):this.props.children}}const ae=e=>(0,q.Y)(ee,{...e,children:(0,q.Y)(Z,{...e})}),te=i.I4.header`
  ${({theme:e})=>`\n      background-color: ${e.colors.grayscale.light5};\n      margin-bottom: 2px;\n      z-index: 10;\n\n      &:nth-last-of-type(2) nav {\n        margin-bottom: 2px;\n      }\n      .caret {\n        display: none;\n      }\n      .navbar-brand {\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n        /* must be exactly the height of the Antd navbar */\n        min-height: 50px;\n        padding: ${e.gridUnit}px\n          ${2*e.gridUnit}px\n          ${e.gridUnit}px\n          ${4*e.gridUnit}px;\n        max-width: ${e.gridUnit*e.brandIconMaxWidth}px;\n        img {\n          height: 100%;\n          object-fit: contain;\n        }\n        &:focus {\n          border-color: transparent;\n        }\n        &:focus-visible {\n          border-color: ${e.colors.primary.dark1};\n        }\n      }\n      .navbar-brand-text {\n        border-left: 1px solid ${e.colors.grayscale.light2};\n        border-right: 1px solid ${e.colors.grayscale.light2};\n        height: 100%;\n        color: ${e.colors.grayscale.dark1};\n        padding-left: ${4*e.gridUnit}px;\n        padding-right: ${4*e.gridUnit}px;\n        margin-right: ${6*e.gridUnit}px;\n        font-size: ${4*e.gridUnit}px;\n        float: left;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n\n        span {\n          max-width: ${58*e.gridUnit}px;\n          white-space: nowrap;\n          overflow: hidden;\n          text-overflow: ellipsis;\n        }\n        @media (max-width: 1127px) {\n          display: none;\n        }\n      }\n      @media (max-width: 767px) {\n        .navbar-brand {\n          float: none;\n        }\n      }\n      @media (max-width: 767px) {\n        .antd5-menu-item {\n          padding: 0 ${6*e.gridUnit}px 0\n            ${3*e.gridUnit}px !important;\n        }\n        .antd5-menu > .antd5-menu-item > span > a {\n          padding: 0px;\n        }\n        .main-nav .antd5-menu-submenu-title > svg:nth-of-type(1) {\n          display: none;\n        }\n      }\n  `}
`,{SubMenu:ne}=c.NG,le=(0,i.I4)(ne)`
  ${({theme:e})=>o.AH`
    [data-icon="caret-down"] {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.xs}px;
      margin-left: ${e.gridUnit}px;
    }
    &.antd5-menu-submenu {
        padding: ${2*e.gridUnit}px ${4*e.gridUnit}px;
        display: flex;
        align-items: center;
        height: 100%;  &.antd5-menu-submenu-active {
    .antd5-menu-title-content {
      color: ${e.colors.primary.base};
    }
  }
  `}
`,{useBreakpoint:re}=d.xA;function ie({data:{menu:e,brand:a,navbar_right:t,settings:n,environment_tag:i},isFrontendRoute:o=()=>!1}){const[f,_]=(0,r.useState)("horizontal"),y=re(),x=(0,b.Q1)();let Y;(0,r.useEffect)((()=>{function e(){window.innerWidth<=767?_("inline"):_("horizontal")}e();const a=l()((()=>e()),10);return window.addEventListener("resize",a),()=>window.removeEventListener("resize",a)}),[]),function(e){e.Explore="/explore",e.Dashboard="/dashboard",e.Chart="/chart",e.Datasets="/tablemodelview"}(Y||(Y={}));const w=[],[C,S]=(0,r.useState)(w),A=(0,u.zy)();return(0,r.useEffect)((()=>{const e=A.pathname;switch(!0){case e.startsWith(Y.Dashboard):S(["Dashboards"]);break;case e.startsWith(Y.Chart)||e.startsWith(Y.Explore):S(["Charts"]);break;case e.startsWith(Y.Datasets):S(["Datasets"]);break;default:S(w)}}),[A.pathname]),(0,s.P3)(v.vX.standalone)||x.hideNav?(0,q.Y)(q.FK,{}):(0,q.Y)(te,{className:"top",id:"main-menu",role:"navigation",children:(0,q.FD)(d.fI,{children:[(0,q.FD)(d.fv,{md:16,xs:24,children:[(0,q.Y)(h.m_,{id:"brand-tooltip",placement:"bottomLeft",title:a.tooltip,arrow:{pointAtCenter:!0},children:o(window.location.pathname)?(0,q.Y)(m.K,{className:"navbar-brand",to:a.path,children:(0,q.Y)("img",{src:a.icon,alt:a.alt})}):(0,q.Y)("a",{className:"navbar-brand",href:a.path,tabIndex:-1,children:(0,q.Y)("img",{src:a.icon,alt:a.alt})})}),a.text&&(0,q.Y)("div",{className:"navbar-brand-text",children:(0,q.Y)("span",{children:a.text})}),(0,q.Y)(c.NG,{mode:f,"data-test":"navbar-top",className:"main-nav",selectedKeys:C,disabledOverflow:!0,children:e.map(((e,a)=>{var t;return(({label:e,childs:a,url:t,index:n,isFrontendRoute:l})=>t&&l?(0,q.Y)(c.NG.Item,{role:"presentation",children:(0,q.Y)(p.k2,{role:"button",to:t,activeClassName:"is-active",children:e})},e):t?(0,q.Y)(c.NG.Item,{children:(0,q.Y)("a",{href:t,children:e})},e):(0,q.Y)(le,{title:e,icon:"inline"===f?(0,q.Y)(q.FK,{}):(0,q.Y)(g.F.CaretDownOutlined,{iconSize:"xs"}),children:null==a?void 0:a.map(((a,t)=>"string"==typeof a&&"-"===a&&"Data"!==e?(0,q.Y)(c.NG.Divider,{},`$${t}`):"string"!=typeof a?(0,q.Y)(c.NG.Item,{children:a.isFrontendRoute?(0,q.Y)(p.k2,{to:a.url||"",exact:!0,activeClassName:"is-active",children:a.label}):(0,q.Y)("a",{href:a.url,children:a.label})},`${a.label}`):null))},n))({index:a,...e,isFrontendRoute:o(e.url),childs:null==(t=e.childs)?void 0:t.map((e=>"string"==typeof e?e:{...e,isFrontendRoute:o(e.url)}))})}))})]}),(0,q.Y)(d.fv,{md:8,xs:24,children:(0,q.Y)(ae,{align:y.md?"flex-end":"flex-start",settings:n,navbarRight:t,isFrontendRoute:o,environmentTag:i})})]})})}function oe({data:e,...a}){const t={...e},n={Data:!0,Security:!0,Manage:!0},l=[],r=[];return t.menu.forEach((e=>{if(!e)return;const a=[],t={...e};var i;e.childs&&(e.childs.forEach((e=>{("string"==typeof e||e.label)&&a.push(e)})),t.childs=a),n.hasOwnProperty(e.name)?((null==(i=t.childs)?void 0:i.length)||0)>0&&r.push(t):l.push(t)})),t.menu=l,t.settings=r,(0,q.Y)(ie,{data:t,...a})}},85994:(e,a,t)=>{t.d(a,{A:()=>p});var n=t(96540),l=t(96453),r=t(67073),i=t(2445);const o=l.I4.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,s=(0,l.I4)(r.F.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,d=(0,l.I4)(r.F.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,c=(0,l.I4)(r.F.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,h=l.I4.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,u=l.I4.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,p=(0,n.forwardRef)((({indeterminate:e,id:a,checked:t,onChange:l,title:r="",labelText:p="",...m},g)=>{const b=(0,n.useRef)(),v=g||b;return(0,n.useEffect)((()=>{v.current.indeterminate=e}),[v,e]),(0,i.FD)(i.FK,{children:[(0,i.FD)(u,{children:[e&&(0,i.Y)(s,{}),!e&&t&&(0,i.Y)(c,{}),!e&&!t&&(0,i.Y)(d,{}),(0,i.Y)(h,{name:a,id:a,type:"checkbox",ref:v,checked:t,onChange:l,...m})]}),(0,i.Y)(o,{title:r,htmlFor:a,children:p})]})}))}}]);