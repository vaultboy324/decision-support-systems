import React from "react";
import BootstrapTable from 'react-bootstrap-table-next';
import {Container} from "react-bootstrap";

import './shifted_ideal.css'

const constants = require('../../const/const');

class ShiftedIdeal extends React.Component{
    state = {
        best_alternative: [],
        matrix: [],
        ordered_table: [],
        report: [],
        priority_levels: []
    };

    constructor(props) {
        super(props);
    }

    async componentDidMount() {
        const response = await fetch('http://localhost:5000/shifted_ideal');
        const result = await response.json();
        this.setState({
            best_alternative: [result.best_alternative],
            matrix: result.matrix,
            ordered_table: result.ordered_table,
            report: result.report,
            priority_levels: [result.priority_levels]
        });
        console.log(result)
    }

    render() {
        return <Container>
            {/*<BootstrapTable keyField='id' columns={this.state.columns} data={this.state.data}/>*/}
            <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                            columns={constants.decision_support_columns}
                            data={this.state.priority_levels}
                            bordered={true}
                            caption={constants.texts.priority_levels}/>
            <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                            columns={constants.decision_support_columns}
                            data={this.state.matrix}
                            bordered={true}
                            caption={constants.texts.matrix}/>

            {
                this.state.report.map((element, index) => {
                    return(<Container className={'list'}>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={[element.ideal]}
                                        bordered={true}
                                        caption={constants.texts.ideal_object}/>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={[element.defective]}
                                        bordered={true}
                                        caption={constants.texts.defective_object}/>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={element.relative_units}
                                        bordered={true}
                                        caption={constants.texts.relative_units}/>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={[element.complex_importance.entropy]}
                                        bordered={true}
                                        caption={constants.texts.entropy}/>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={[element.complex_importance.expert_assessment]}
                                        bordered={true}
                                        caption={constants.texts.expert_assessment}/>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={[element.complex_importance.complex_importance]}
                                        bordered={true}
                                        caption={constants.texts.complex_importance}/>
                        <BootstrapTable keyField={constants.distance_table_columns[0].dataField}
                                        columns={constants.distance_table_columns}
                                        data={element.distance_table}
                                        bordered={true}
                                        caption={constants.texts.distance_table}/>
                        <BootstrapTable keyField={constants.range_distance_table_columns[0].dataField}
                                        columns={constants.range_distance_table_columns}
                                        data={element.ranged_distance_table}
                                        bordered={true}
                                        caption={constants.texts.ranged_distance_table}/>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={[element.worst_alternative]}
                                        bordered={true}
                                        caption={constants.texts.worst_alternative}/>
                        <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                                        columns={constants.decision_support_columns}
                                        data={element.matrix}
                                        bordered={true}
                                        caption={constants.texts.matrix}/>
                    </Container>)
                })
            }

            <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                            columns={constants.decision_support_columns}
                            data={this.state.ordered_table}
                            bordered={true}
                            caption={constants.texts.ordered_table}/>
            <BootstrapTable keyField={constants.decision_support_columns[0].dataField}
                            columns={constants.decision_support_columns}
                            data={this.state.best_alternative}
                            bordered={true}
                            caption={constants.texts.best_alternative}/>
        </Container>
    }
}

export default ShiftedIdeal;