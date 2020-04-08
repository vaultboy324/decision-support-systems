import React from "react";
import BootstrapTable from "react-bootstrap-table-next";

import './Page.css'

const constants = require('../../const/const')

class Page extends React.Component{
    state = {
        method: '',
        prefersTable: {
            table: [],
            parameters: []
        },
        pairedComparisons: {
            comparisons: [],
        },
        levels: [],
        percents: [],
        bestAlternative: 0,

    };

    constructor() {
        super();
    }

    async componentDidMount(){
        let id = this.props.match.params.method;
        console.log(id);
        this.setState({
            method: constants.texts[id]
        });
        const response = await fetch(`http://localhost:5000/${id}`);
        const result = await response.json();
        this.setState({
            prefersTable: this._createViewTable(result.prefersTable)
        });
        this.setState({
            pairedComparisons: this._createPairedComparisons(result.pairedComparisons)
        });
        this.setState({
            levels: this._createLevelsTable(result.levels)
        })
        this.setState({
            percents: this._createPercentsList(result.levels)
        });
        console.log(this.state);
    }

    _createPercentsList(responseLevels){
        let lastLevel = responseLevels[responseLevels.length - 1];
        let percents = [];
        let bestAlternative = lastLevel.indexOf(Math.max.apply(null, lastLevel)) + 1;
        this.setState({
            bestAlternative
        })

        lastLevel.forEach((value, index)=>{
           percents.push(`${value * 100}%`);
        });

        console.log(percents);

        return percents;
    }

    _createLevelsTable(responseLevels){
        let index = 0;
        let values = [];
        responseLevels.forEach((level, levelNumber)=>{
           level.forEach((value, valueNumber)=>{
               let row = {}
               row[constants.fields.levelNumber] = `z${index + 1}`;
               row[constants.fields.value] = value;
               ++index;
               values.push(row)
           });
        });
        return values;
    }

    _createPairedComparisons(responseComparisons){
        let comparisonsTable = [];
        // let columns = constants.tables.comparison_table.columns;

        console.log(responseComparisons);

        responseComparisons.forEach((comparison, index)=>{
            comparisonsTable.push(this._createComparisonTable(comparison, index))
        });

        console.log(comparisonsTable);

        return {
            comparisons: comparisonsTable
        }
    }

    _createComparisonTable(currentComparison, index){
        let data = [];
        let field = constants.fieldList[index];
        let columns = JSON.parse(JSON.stringify(constants.tables.comparison_table.columns));

        currentComparison[field].forEach((row, index)=>{
            let newRow = {};
            columns.push({
                "dataField": index.toString(),
                "text": index.toString()
            });
            row.forEach((element, rowIndex)=>{
                newRow[rowIndex.toString()] = element;
            });
            newRow[constants.fields.normingValues] = currentComparison.parameters[constants.fields.normingValues][index];
            newRow[constants.fields.alternative] = index;
            data.push(newRow);

        })

        console.log(columns);

        columns.push({
            "dataField": constants.fields.normingValues,
            "text": constants.texts.norming_values
        })

        return {
            data,
            title: constants.texts[field],
            parameters: [currentComparison.parameters],
            columns
        }
    }

    _createViewTable(responseTable){
        let mainTable = [];

        constants.fieldList.forEach((field, index)=>{
            let row = responseTable[field];
            row[constants.fields.fieldName] = constants.texts[field];
            row[constants.fields.normingValues] = responseTable[constants.fields.parameters][constants.fields.normingValues][index]
            mainTable.push(row);
        })

        return {
            table: mainTable,
            parameters: [responseTable.parameters]
        }

        // this.setState({
        //     prefersTable: {
        //         table: mainTable,
        //         parameters: [responseTable.parameters]
        //     }
        // })

        // responseTable.forEach((element, index)=>{
        //
        // })
    }

    render() {
        return (
            <div>
                <div className={"block"}>
                    <h1>Выбранный метод: {`${this.state.method}`}</h1>
                </div>
                <div className={"block"}>
                    <BootstrapTable keyField={constants.tables.prefers_table.columns[0].dataField}
                                    columns={constants.tables.prefers_table.columns}
                                    data={this.state.prefersTable.table}
                                    bordered={true}
                                    caption={constants.tables.prefers_table.title}/>
                    <BootstrapTable keyField={constants.tables.parameters_table.columns[0].dataField}
                                    columns={constants.tables.parameters_table.columns}
                                    data={this.state.prefersTable.parameters}
                                    bordered={true}/>
                </div>
                {
                    this.state.pairedComparisons.comparisons.map((comparison, index)=> {
                        return (
                            <div className={"block"}>
                                <BootstrapTable keyField={constants.tables.comparison_table.columns[0].dataField}
                                                columns={comparison.columns}
                                                data={comparison.data}
                                                caption={comparison.title}
                                                bordered={true}
                                />
                                <BootstrapTable keyField={constants.tables.parameters_table.columns[0].dataField}
                                                columns={constants.tables.parameters_table.columns}
                                                data={comparison.parameters}
                                                bordered={true}/>
                            </div>
                        )
                    })
                }
                <div className={"block"}>
                    <BootstrapTable keyField={constants.tables.levelsTable.columns[0].dataField}
                                    columns={constants.tables.levelsTable.columns}
                                    data={this.state.levels}
                                    bordered={true}
                                    caption={constants.tables.levelsTable.title}/>
                </div>
                <div className={"block"}>
                    {
                        this.state.percents.map((percent, index)=>{
                            return(<p>Значение {index + 1}-ой альтернативы в процентах: {percent}</p>)
                        })
                    }
                </div>
                <div className={"block"}>
                    {
                        <p>Номер лучшей альтернативы: {`${this.state.bestAlternative}`}</p>
                    }
                </div>
            </div>
        )
    }
}

export default Page;