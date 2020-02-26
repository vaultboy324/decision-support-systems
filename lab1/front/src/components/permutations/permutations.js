import React from "react";
import BootstrapTable from 'react-bootstrap-table-next';
import {Container} from "react-bootstrap";

import './permutations.css'

const constants = require('../../const/const');

class Permutations extends React.Component{
    state =  {
        best_alternative: {},
        complex_importance: {},
        matrix: [],
        ordered_table: [],
        permutation_list: [],
        priority_levels: {},
    };
    async componentDidMount() {
        const response = await fetch("http://localhost:5000/permutations");
        const result = await response.json();
        console.log(result);
        this.setState(result)
    }

    render() {
        return (
            <Container>
                <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                columns={constants.decision_support_columns}
                                data={[this.state.priority_levels]}
                                bordered={true}
                                caption={constants.texts.priority_levels}/>
                <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                columns={constants.decision_support_columns}
                                data={this.state.matrix}
                                bordered={true}
                                caption={constants.texts.matrix}/>
                <BootstrapTable keyField={constants.permutation_list_columns[0].dataField}
                                columns={constants.permutation_list_columns}
                                data={this.state.permutation_list}
                                bordered={true}
                                caption={constants.texts.permutation_list}/>
                <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                columns={constants.decision_support_columns}
                                data={this.state.ordered_table}
                                bordered={true}
                                caption={constants.texts.ordered_table}/>
                <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                columns={constants.decision_support_columns}
                                data={[this.state.best_alternative]}
                                bordered={true}
                                caption={constants.texts.best_alternative}/>
            </Container>
        )
    }
}

export default Permutations