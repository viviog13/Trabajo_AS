import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';  // nuevo
import UsersList from './component/UsersList';
import AddUser from './component/AddUser';
 
 
class App extends Component {
  // nuevo
  constructor() {
    super();
    this.state = {
       users: [],
       titulo: '',
       autor: '',
       añodepublicacion: '',
       editorial: '',
       generoliterario: '',
     };
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
  };
  // nuevo
  componentDidMount() {
  this.getUsers();
  };
  getUsers() {
   axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)  // nuevo
   .then((res) =>{ this.setState({ users: res.data.data.users }); })
   .catch((err) =>{ console.log(err); });
  };

  addUser(event) {
    event.preventDefault();
    // new
    const data = {
      titulo: this.state.titulo,
      autor: this.state.autor,
      añodepublicacion: this.state.añodepublicacion,
      editorial: this.state.editorial,
      generoliterario: this.state.generoliterario
    };
    // new
     axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then((res) => {
        this.getUsers();  // nuevo
        this.setState({ titulo: '', autor: '', añodepublicacion: '', editorial: '', generoliterario: '' });
      })
      .catch((err) => { console.log(err); });
    };

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-half">  {/* new */}
              <br/>
              <h1 className="title is-1">All Users</h1>
              <hr/><br/>
              <AddUser
                titulo={this.state.titulo}
                autor={this.state.autor}
                añodepublicacion={this.state.añodepublicacion}
                editorial={this.state.editorial}
                generoliterario={this.state.generoliterario}
                addUser={this.addUser}
                handleChange={this.handleChange}
              />
              <br/><br/>  {/* new */}
              <UsersList users={this.state.users}/>
            </div>
          </div>
        </div>
      </section>
    )
  }
};
 
ReactDOM.render(
  <App />,
  document.getElementById('root')
);