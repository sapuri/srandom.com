import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import TextField from 'material-ui/TextField';
import Checkbox from 'material-ui/Checkbox';
import Toggle from 'material-ui/Toggle';

export default class ModalDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            is_active: this.props.is_active,
            new_record: {
                medal: this.props.record.medal,
                bad_count: this.props.record.bad_count,
                updated_at: this.props.record.updated_at
            }
        };
        this._handleCloseDialog = this._handleCloseDialog.bind(this);
        this._handleChangeMedal = this._handleChangeMedal.bind(this);
        this._handleChangeBadCount = this._handleChangeBadCount.bind(this);
        this._saveRecord = this._saveRecord.bind(this);
        this._deleteRecord = this._deleteRecord.bind(this);
    }

    _handleCloseDialog() {
        this.setState({ is_active: false });
    }

    _handleChangeMedal(event) {
        this.setState({
            new_record: {
                medal: event.target.value,
                bad_count: this.state.new_record.bad_count,
                updated_at: this.state.new_record.updated_at
            }
        });
        console.log(event.target.value);
    }

    _handleChangeBadCount(event) {
        let validated_bad_count;
        if (event.target.value < 0) validated_bad_count = 0;
        else if (event.target.value > 200) validated_bad_count = 200;
        else validated_bad_count = event.target.value;

        this.setState({
            new_record: {
                medal: this.state.new_record.medal,
                bad_count: validated_bad_count,
                updated_at: this.state.new_record.updated_at
            }
        });
    }

    _saveRecord() {
        // TODO: Ajaxで記録を更新

        this.setState({
            is_active: false,
            new_record: {
                medal: this.state.new_record.medal !== null ? this.state.new_record.medal : 12,
                bad_count: this.state.new_record.bad_count,
                updated_at: this.state.new_record.updated_at
            }
        });
    }

    _deleteRecord() {
        // TODO: Ajax で記録を削除

        this.setState({
            is_active: false,
            new_record: {
                medal: null,
                bad_count: null,
                updated_at: null
            }
        });
    }

    /* Stateを初期化 */
    _initializeState() {
        this.setState({
            is_active: this.props.is_active,
            new_record: {
                medal: this.props.record.medal,
                bad_count: this.props.record.bad_count,
                updated_at: this.props.record.updated_at
            },
            is_updated: false
        });
    }

    /* Propが更新される度に実行 */
    componentWillReceiveProps(nextProps) {
        this._initializeState();
    }

    render() {
        const actions = [
            <FlatButton label="キャンセル" onTouchTap={this._handleCloseDialog} />,
            <FlatButton label="削除" secondary={true} onTouchTap={this._deleteRecord} />,
            <FlatButton label="更新" primary={true} onTouchTap={this._saveRecord} />,
        ];

        if (this.state.is_active === false) return null;

        console.log(this.state.new_record);

        return (
            <Dialog
                title={`${this.props.title} (${this.props.difficulty})`}
                actions={actions}
                modal={false}
                open={this.state.is_active}
                onRequestClose={this._handleCloseDialog}
            >
                <p><a href={`/ranking/detail/${this.props.id}/`}>ランキングを見る</a></p>
                <SelectField floatingLabelText="クリアメダル" value={this.state.new_record.medal ? this.state.new_record.medal : 12} onChange={this._handleChangeMedal}>
                    <MenuItem value={1} primaryText="パーフェクト" />
                    <MenuItem value={2} primaryText="フルコンボ ☆" />
                    <MenuItem value={3} primaryText="フルコンボ ◇" />
                    <MenuItem value={4} primaryText="フルコンボ ○" />
                    <MenuItem value={5} primaryText="クリア ☆" />
                    <MenuItem value={6} primaryText="クリア ◇" />
                    <MenuItem value={7} primaryText="クリア ○" />
                    <MenuItem value={8} primaryText="未クリア ☆" />
                    <MenuItem value={9} primaryText="未クリア ◇" />
                    <MenuItem value={10} primaryText="未クリア ○" />
                    <MenuItem value={11} primaryText="イージー" />
                    <MenuItem value={12} primaryText="未プレイ" />
                </SelectField>
                <br />
                <TextField floatingLabelText="BAD数" type="number" value={this.state.new_record.bad_count} onChange={this._handleChangeBadCount} />
                <br />
                <Checkbox label="ハード" checked={false} />
                <br />
                <Toggle label="更新内容をツイートする" labelPosition="right" />
            </Dialog>
        );
    }
}
ModalDialog.propTypes = {
    is_active: React.PropTypes.bool.isRequired,
    id: React.PropTypes.number.isRequired,
    title: React.PropTypes.string.isRequired,
    difficulty: React.PropTypes.string.isRequired,
    record: React.PropTypes.object.isRequired
};