import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
 
import UsersList from '../UsersList';
 
const users = [
  {
	'active': true,
	'autor': 'Susi',
	'id': 1,
	'titulo': 'Mil caeran',
	'añodepublicacion': '1990',
	'editorial': 'Ni idea',
	'generoliterario': 'Accion'
  },
  {
	'active': true,
	'autor': 'Mario',
	'id': 2,
	'titulo': 'La casa verde',
	'añodepublicacion': '1966',
	'editorial': 'Six Barral',
	'generoliterario': 'Ficcion'
  }
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('Mil caeran');
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});
