import React from 'react';

/* ローディング中のアニメーション */
export default class Loader extends React.Component {
    render() {
        if (this.props.is_active === false) return null;
        return (
            <div id="loader" style={{textAlign: "center"}}>
                <i className="fa fa-refresh fa-spin fa-3x"></i>
            </div>
        )
    }
}
Loader.propTypes = { is_active: React.PropTypes.bool.isRequired };
