import React, { useState, useRef, Component } from 'react';
import axios from 'axios';
import './App.css';
import { CSVLink, CSVDownload } from "react-csv";
import About from './components/About';
import Login from './components/Login';
import Iframe from './components/Iframe';
import Protected from './components/Protected';
import Logout from './components/Logout';
import Switch from "react-switch";

import {
	BrowserRouter as Router,
	Routes,
	Route,
	Link
} from 'react-router-dom';

class SwitchExample extends Component {
  constructor() {
    super();
    this.state = { checked: false };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(checked) {
    this.setState({ checked });
  }

  render() {
    return (
      <label>
        <Switch 
          onChange={this.handleChange} 
          checked={this.state.checked} 
          uncheckedIcon={
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100%",
                fontSize: 15,
                color: "orange",
                paddingRight: 2
              }}
            >
              Off
            </div>
          }
          checkedIcon={
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100%",
                fontSize: 15,
                color: "orange",
                paddingRight: 2
              }}
            >
              On
            </div>
          }

        />
      </label>
    );
  }
}

function SearchBar() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [sql_result,setSqlResult] = useState([[]]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showtable, setShowTable] = useState(false);
  const [showcode, setShowCode] = useState(false);
  const [showtwobox,setShowtwobox] = useState(false);
  const [is_run,setIsRun] = useState(true);
  const [opacity_val,setOpacity] = useState(0);
  const [showScroll,setShowScroll] = useState(true);
  const [isLoading_block2, setisLoading_block2] = useState(false);
  const tableRef = useRef(null);
  const [isOn, setIsOn] = useState(false);
  const [is_chart_in_res, setIsChartInRes] = useState(false);
  console.log(process.env.REACT_APP_SGNONS);

  const handleSearch = async (e) => {
    //showtwobox?console.log("donothing"):document.getElementById("home-blob").remove();
    handleShowQuestions()
    console.log(query);
    e.preventDefault();
    setIsLoading(true);
    
    
    setShowTable(false);
    setError(null);
    try {
      setIsLoading(true);  
      setIsRun(true);
      // const res = await axios.post('http://51.142.115.5:5000/generate_sql_query', { prompt:query });
      // const res = await axios.post('http://127.0.0.1:50001/generate_sql_query', { prompt:query });
      const res = await axios.post('http://'+ process.env.REACT_APP_HOST +':'+ process.env.REACT_APP_PORT +'/generate_sql_query', { prompt:query });  
      console.log(res);
      
      setResult(res.data.query);
      setIsRun(res.data.is_run)
      if (res.data.is_run)
      {  
        setResult(res.data.query);
        setSqlResult(res.data.jsonresult);
        setIsChartInRes(res.data.is_chart_in_ans)
      }
      else
      {
        setIsRun(false)
        setError(res.data.error_details);
        console.log("erorr :   :"+error)
        setShowTable(false)
      }     
    } catch (err) {
      setError(err.message);
      console.log(err);
    }
    setIsLoading(false)
    setisLoading_block2(true);
    await new Promise(resolve => setTimeout(resolve, 1500 + Math.floor(Math.random() * 3)*1000 )); // 3 sec
    if (is_run)
    {
      setShowTable(true)
    }
    setisLoading_block2(false)
    
  };
  function handleShowQuestions()
  {
    setShowtwobox(true)
    console.log("inside click input"+showtwobox)
  }

  function DynamicTable()
  {
    const TableData = sql_result[0][0];
    console.log("Table data",TableData[0])
      if (TableData[0]['avg']){
        setShowScroll(false)
        return(
          <>
          <div className="col-12 mt-2 mb-2 results-2 pb-2" >Avg Value : {TableData[0]['avg'].toLocaleString("en-US")}</div>
          </>
        )
      
    }

    // get table column
    console.log("Tabledata : : "+TableData);
     const column = Object.keys(TableData[0]);
     console.log("keys"+column);
      const columns = column;
     // get table heading data
     const ThData =()=>{
      return column.map((dataR)=>{
      return <th scope="col" key={dataR}>{dataR}</th>
      })
     }
    
    // get table row data
    const tdData =() =>{
      return TableData.map((dataR)=>{
        return(
          <tr>
          {
            column.map((v)=>{
            return <td>{
            typeof dataR[v] === 'number'?
            dataR[v].toLocaleString("en-US")                    
            :
            typeof dataR[v] === 'string'? dataR[v].length>10 & dataR[v].length<30?dataR[v].slice(0, 28)+"...":dataR[v].slice(0, 10)+"...":
            dataR[v]+""
          }
          </td>
          })}
          </tr>)
         })
       }
      return (
        <table className="table table-hover table-striped table-responsive" ref={tableRef}>
          <thead>
            <tr>{ThData()}</tr>
          </thead>
          <tbody className='tbody'>
            {tdData()}
          </tbody>  
        </table>
      )
    }  
  function InputField()
  {
    return
    (
      <>
      {
        showtwobox? 
          <></>
          :
          <></>
      }
      </>
    );
  }
  function showCodeInCard()
  {
    showcode?setShowCode(false):setShowCode(true)
      
  }
  function loadHtml(id, filename)
  {
    console.log(`div id: ${id}, filename: ${filename}`);
    let xhhtp;
    let element = document.getElementById;
    let file = filename;

    if (file){
      xhhtp = new XMLHttpRequest();
      xhhtp.onreadystatechange = function (){
        if(this.readyState === 4 ){
          if(this.status === 200){element.innerHTML = this.responseText;}
          if(this.status === 404){element.innerHTML = "<h1>Page Not Found</h1>";}
          
        }
      }
      xhhtp.open("Get", `src/${file}`,true);
      xhhtp.send();
      return;  

    }
  }

  const handleToggle = () => {
    setIsOn(!isOn);
  }

  const get_chart_url =  () =>{
    // await new Promise(resolve => setTimeout(resolve, 1500 + Math.floor(Math.random() * 3)*1000 ));
    console.log(process.env.REACT_APP_CHART_URL);
    return 'http://localhost:8081/templates/chart.html';
  }


  return(
    <>             
    {/* -- Second page iframe and search bar -- */}
    {showtwobox? 
      <div class="container mt-5">
        <div class="row d-flex justify-content-center">
          {/* -- Second Page Iframe  -- */}
          <Iframe classes='d-flex iframeclass-page2' />
            <div class="col-lg-6 col-md-8 col-sm-11 col-11">
              <div class="search rounded-pill mt-3 search-mob-p2">
                {/* -- Second Page Search bar  -- */}
                <form>
                  <i class="fa fa-search"></i>
                    <input  type="text"  class="form-control rounded-pill" placeholder="How can I help?" value={query} onChange={(e) => setQuery(e.target.value)}/>
                      <button class="btn text-white" onClick={handleSearch}>
                        <i className="fa fa-arrow-right" aria-hidden="true"></i>
                      </button>
                </form>
              </div>
            </div>
        </div>
      </div>
      :<>
      {/* -- First page iframe and search bar -- */}
      <div class="col-lg-12 col-md-12 col-sm-12 col-12 d-flex justify-content-center align-items-center" id="home-blob">
          {/* -- First Page Iframe  -- */}
        <Iframe classes='iframeclass-page1 lazyload' />
      </div>
      <div class="container mt-5 container-ipad">      
        <div class="row height d-flex justify-content-center align-items-center ">
          <div class="col-lg-8 col-md-9 col-sm-10 col-11  mb-4">
            <div class="search rounded-pill">
              {/* -- First Page Search bar  -- */}
              <form>
                <i class="fa fa-search"></i>
                <input  type="text" class="form-control rounded-pill" placeholder="How can I help?" value={query} onChange={(e) => setQuery(e.target.value)}/>
                <button class="btn text-white" onClick={handleSearch}>
                  <i className="fa fa-arrow-right" aria-hidden="true"></i> 
                </button>
              </form>    
            </div>
          </div>
        </div>
      </div>
      </>
    }
    {
    showtwobox?  
    <>
    {/* -- Second Page Code Card (1) -- */}
      <div class="container col-lg-12 col-md-12 col-sm-12 col-12 d-flex justify-content-center align-items-center top-card">
        <div class="card">
          <div class="card-body">
            <div class="row">
               {/* -- Heading For Card Query -- */}
              <div class="col-lg-12 col-md-12 col-sm-12 col-12">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-terminal text-success" viewBox="0 0 16 16">
                    <path d="M6 9a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3A.5.5 0 0 1 6 9zM3.854 4.146a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2z"/>
                    <path d="M2 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h12z"/>
                  </svg>
                  <button class="btn btn fw-bold fw-normal fs-6 ms-1">Code</button>
               
                  {/* -- Loading Spinner Button -- */}
                  <button class="btn btn fw-bold fw-normal fs-6 ms-1">
                    {isLoading?
                      <span className='justify-content-center align-items-center position-absolute start-50 translate-middle'>   
                        <i class="fa fa-spinner fa-spin "></i>   
                      </span>
                      :
                      <></>
                    }
                  </button>
                  {/* -- Toggle Button (Show/Hide) -- */}
                  <button className="btn  btn-sm text-success fw-normal fs-6 ms-2 float-end ani" onClick={showCodeInCard}>{ showcode & result.length >0 ? isLoading? <></> :<>Hide</>: isLoading? <></> : <>Show</>}</button>
              </div>
              {showcode & result.length >0 ? isLoading? <></> :  
             <div className="col-lg-12 col-md-12 col-sm-12 col-12 mt-0 results"><pre>{result}</pre></div>:<></>}
            </div>
          </div>
        </div>
      </div>
    {/* -- Second Page Code Card (2) -- */}
      <div class="container col-lg-12 col-md-12 col-sm-12 col-12 d-flex justify-content-center align-items-center mt-4">
        <div class="card">
          <div class="card-body ">
            <div class="row">
              {/*Iris heading Column*/}      
              <div class="col-lg7 col-md-7 col-sm-7 col-7 align-self-start">
                <object data="nebulus.svg" width="22" height="22"></object>
                <button class="btn btn fw-bold fw-normal fs-6 mb-3 ms-1">{is_run?<> Iris</>:<>Error</>}  </button>      
              </div>
              <div class="col-lg-5 col-md-5 col-sm-5 col-5 align-self-end ">
                <div class=" align-self-end  ">
                 { is_chart_in_res ?                  
                      <div class="switch-field">
                        <div className='field-group' field-data="Chart">
                          <input type='checkbox' name='checkbox' id="switch" class="checkbox-field" onChange={handleToggle}></input>
                          <label for="switch" class="checkbox-label"><span>Dataset</span></label>
                        </div>
                      </div>
                  :<></>
                  
                  }
                    {is_run & showtable?
                    sql_result.length === 1 ?
                    sql_result[0].length === 1?
                    sql_result[0][0].length > 0?
                    <>
                    {console.log("error before  csvlink")}
                    <CSVLink data={sql_result[0][0]}>
                    {/*Download Button*/}
                    <button class="btn  btn-sm fw-bold bg-success fw-normal fs-6 ms-0 float-end iris-card-button" >
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-cloud-download text-white mx-0" viewBox="0 0 16 16">
                        <path d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
                        <path d="M7.646 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V5.5a.5.5 0 0 0-1 0v8.793l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z"/>
                      </svg>
                    </button>   
                    </CSVLink>
                    </>
                    :<></>
                    :<></>
                    :<></>
                    :
                    <button class="btn  btn-sm fw-bold fw-normal bg-success fs-6 float-end iris-card-button" >
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-cloud-download text-white mx-0" viewBox="0 0 16 16">
                        <path d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
                        <path d="M7.646 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V5.5a.5.5 0 0 0-1 0v8.793l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z"/>
                      </svg>
                    </button>   
                    }
                        
                  {/*Send mail*/}
                  <button class="btn  btn-sm fw-bold fw-normal bg-success fs-6  iris-card-button float-end">
                    <a href={"mailto:person@company.com?subject="+{query}+"&body="+{result} }>
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-send text-white " viewBox="0 0 16 16">
                          <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576 6.636 10.07Zm6.787-8.201L1.591 6.602l4.339 2.76 7.494-7.493Z"/>
                        </svg>
                    </a>    
                  </button>
                  </div>
                  </div>
                <div>
                  <div style={{ display: isOn ? "none" : "block" }}>
                    {/*Table Data Show*/}
                    <div className={ showScroll ?'col tables':'col'}> 
                      { is_run & showtable ?
                      sql_result.length === 1 ?
                      sql_result[0].length === 1?
                      sql_result[0][0].length > 0?
                        <><DynamicTable />  </>
                        :<>No data, Please Try again </>
                        :<>No data Please Try again </>
                        :<>No data Please Try again </>
                        :<>{is_run?<> 
                        { isLoading_block2?
                        <button class="btn btn fw-bold fw-normal fs-6 ms-1 ">
                          <span className='justify-content-center align-items-center position-absolute start-50 translate-middle delay-2' >
                            <i class="fa fa-spinner fa-spin "></i>
                          </span>          
                        </button>
                        :  
                        showtable?
                        <>No data Please Try again</>
                        : <></>
                        }      
                        </>:<pre> {error} </pre>}</>
                      }
                    </div>
                  </div>
                  {
                      isOn?
                    <div style={{ display: "block"}}>
                    
                      {/*Chart Data Show*/}
                      <div id='chart_div' className='chart_div'>
                        <iframe src={get_chart_url()} className='chart_iframe'></iframe>
                      </div>
                    </div> 
                    :
                    <></>
                  }  
                 
                </div>
            </div>
          </div> 
        </div>
      </div>
    
      </>
      :
      <>
      {/* Page 1:- Questions suggestions */}
    
        <div class="container things-container">
   
          <div class="row height d-flex justify-content-center align-items-center">
            {/* -- Things Heading -- */}
            <div class="col-lg-8 col-md-9 col-sm-10 col-10 d-flex ms-5 mb-2 thing-mob">
                <object data="nebulus.svg" width="28" height="25"></object>
                <span class="ms-3 what-txt mb-2">Things you can ask me</span>
              </div>
              <hr/>
              <div class="col-lg-8 col-md-9 col-sm-12 col-12 mt-1 ">
                <div class="row ">
               
                  {/* -- Cards below Things -- */}
                  <div class="col gx-4 ms-3">
                    <div class="p-3 border card-out">
                      <button class="btn btn-sm card-btn " value="Show me all settlements in the last year" onClick={(e) => setQuery(e.target.value)}>
                        Show me all settlements in the last year
                      </button>
                    </div>
                  </div>
                  <div class="col gx-1 ms-2 mx-4">
                    <div class="p-3 border card-out">
                      <button class="btn btn-sm card-btn " value="What is our average settlement?" onClick={(e) => setQuery(e.target.value)}>
                        What is our average settlement?
                      </button>
                    </div>
                  </div>
                </div>
                <div class="row  mt-2">
                  <div class="col gx-4 ms-3">
                    <div class="p-3 border card-out">
                      <button class="btn btn-sm card-btn " value="Show me all hearings in the past 5 years" onClick={(e) => setQuery(e.target.value)}>
                        Show me all hearings in the past 5 years
                      </button>
                    </div>
                  </div>
                  <div class="col gx-1 ms-2 mx-4">
                    <div class="p-3 border card-out">
                      <button class="btn btn-sm card-btn " value="Show me all hearings in the past 3 years" onClick={(e) => setQuery(e.target.value)}>
                        Show me all hearings in the past 3 years
                      </button>
                    </div>
                  </div>
                </div>
                <div class="row  mt-2 ">
                  <div class="col gx-4 ms-3">
                    <div class="p-3 border card-out">
                      <button class="btn btn-sm card-btn " value="Top 10 active arbitrations by revenue" onClick={(e) => setQuery(e.target.value)}>
                        Top 10 active arbitrations by revenue
                      </button>
                    </div>
                  </div>
                  <div class="col gx-1 ms-2 mx-4">
                    <div class="p-3 border card-out">
                      <button class="btn btn-sm card-btn " value="What are the biggest claims in our portfolio?" onClick={(e) => setQuery(e.target.value)}>
                        What are the biggest claims in our portfolio?
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        </div>
      </>
    }  
    </>
  );  
}


export default class App extends Component {
  render() {
    return (
      <>
       <Router>
           <Routes>
                 <Route exact path='/' element={< Protected cmp={ SearchBar } />}></Route>
                 <Route exact path='/about' element={< Protected cmp={ About } />}></Route>
                 <Route exact path='/login' element={<Login/>}></Route>
                 <Route exact path='/logout' element={<Logout />}></Route>
          </Routes>
          
       </Router>


     </>

    )
  }
}