import React from 'react';

const AddUser = (props) => {
  return (
    <form onSubmit={(event) => props.addUser(event)}>
      <div className="field">
        <input
          name="titulo"
          className="input is-large"
          type="text"
          placeholder="Titulo"
          required
          value={props.titulo}  // nuevo
          onChange={props.handleChange}
        />
      </div>
      <div className="field">
        <input
          name="autor"
          className="input is-large"
          type="text"
          placeholder="Autor"
          required
          value={props.autor}  // nuevo
          onChange={props.handleChange}
        />
      </div>
       <div className="field">
        <input
          name="añodepublicacion"
          className="input is-large"
          type="text"
          placeholder="Año de Publicacion"
          required
          value={props.añodepublicacion}  // nuevo
          onChange={props.handleChange}
        />
      </div>
       <div className="field">
        <input
          name="editorial"
          className="input is-large"
          type="text"
          placeholder="Editorial"
          required
          value={props.editorial}  // nuevo
          onChange={props.handleChange}
        />
      </div>
       <div className="field">
        <input
          name="generoliterario"
          className="input is-large"
          type="text"
          placeholder="Genero literario"
          required
          value={props.generoliterario}  // nuevo
          onChange={props.handleChange}
        />
      </div>
      <input
        type="submit"
        className="button is-primary is-large is-fullwidth"
        value="Submit"
      />
    </form>
  )
};

export default AddUser;