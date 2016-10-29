webpackJsonp([0],{

/***/ 0:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _reactDom = __webpack_require__(34);
	
	var _reactDom2 = _interopRequireDefault(_reactDom);
	
	var _MusicList = __webpack_require__(172);
	
	var _MusicList2 = _interopRequireDefault(_MusicList);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	// URLから難易度表とレベルを判定
	var url = window.location.href;
	var split_url = url.split('/');
	var is_srandom = split_url[3] === 'difflist';
	var level = Number(split_url[4]);
	
	// TODO: 記録編集機能を実装
	_reactDom2.default.render(_react2.default.createElement(_MusicList2.default, { lv: level, is_srandom: is_srandom }), document.getElementById('content'));

/***/ },

/***/ 172:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _MusicTable = __webpack_require__(173);
	
	var _MusicTable2 = _interopRequireDefault(_MusicTable);
	
	var _Loader = __webpack_require__(175);
	
	var _Loader2 = _interopRequireDefault(_Loader);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }
	
	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }
	
	var MusicList = function (_React$Component) {
	    _inherits(MusicList, _React$Component);
	
	    function MusicList(props) {
	        _classCallCheck(this, MusicList);
	
	        var _this = _possibleConstructorReturn(this, (MusicList.__proto__ || Object.getPrototypeOf(MusicList)).call(this, props));
	
	        _this.state = {
	            data: [],
	            folder_lamp: 'no-play',
	            loading: true
	        };
	        return _this;
	    }
	
	    _createClass(MusicList, [{
	        key: 'loadMusicList',
	        value: function loadMusicList() {
	            var _this2 = this;
	
	            var max_lv = this.props.is_srandom ? 17 : 50;
	            var url = this.props.is_srandom ? '/api/music/?sran_level=' + (max_lv + 1 - this.props.lv) + '&ordering=level,title' : '/api/music/?level=' + (max_lv + 1 - this.props.lv) + '&ordering=sran_level,title';
	            $.ajax({
	                url: url,
	                dataType: 'json',
	                cache: false,
	                success: function success(data) {
	                    return _this2.setState({
	                        data: data,
	                        loading: false
	                    });
	                },
	                error: function error(xhr, status, err) {
	                    return console.error(status, err.toString());
	                }
	            });
	        }
	    }, {
	        key: 'loadFolderLamp',
	        value: function loadFolderLamp() {
	            var _this3 = this;
	
	            $.ajax({
	                url: '/api/get_folder_lamp/' + this.props.lv + '/',
	                dataType: 'json',
	                data: { is_srandom: this.props.is_srandom },
	                cache: false,
	                success: function success(data) {
	                    return _this3.setState({ folder_lamp: data.folder_lamp });
	                },
	                error: function error(xhr, status, err) {
	                    return console.error(status, err.toString());
	                }
	            });
	        }
	    }, {
	        key: 'componentDidMount',
	        value: function componentDidMount() {
	            this.loadMusicList();
	            this.loadFolderLamp();
	        }
	    }, {
	        key: 'render',
	        value: function render() {
	            return _react2.default.createElement(
	                'div',
	                { id: 'music-list' },
	                _react2.default.createElement(
	                    'h3',
	                    { id: 'lv' + this.props.lv, className: 'level-folder ' + this.state.folder_lamp },
	                    'Lv',
	                    this.props.lv
	                ),
	                _react2.default.createElement(_MusicTable2.default, { data: this.state.data.results, count: this.state.data.count, is_srandom: this.props.is_srandom }),
	                _react2.default.createElement(_Loader2.default, { is_active: this.state.loading })
	            );
	        }
	    }]);
	
	    return MusicList;
	}(_react2.default.Component);
	
	exports.default = MusicList;
	
	MusicList.propTypes = {
	    lv: _react2.default.PropTypes.number.isRequired,
	    is_srandom: _react2.default.PropTypes.bool.isRequired
	};

/***/ },

/***/ 173:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	var _Music = __webpack_require__(174);
	
	var _Music2 = _interopRequireDefault(_Music);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }
	
	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }
	
	var MusicTable = function (_React$Component) {
	    _inherits(MusicTable, _React$Component);
	
	    function MusicTable(props) {
	        _classCallCheck(this, MusicTable);
	
	        var _this = _possibleConstructorReturn(this, (MusicTable.__proto__ || Object.getPrototypeOf(MusicTable)).call(this, props));
	
	        _this.state = {
	            my_account: {
	                id: '',
	                username: ''
	            }
	        };
	        return _this;
	    }
	
	    _createClass(MusicTable, [{
	        key: 'loadMyAccount',
	        value: function loadMyAccount() {
	            var _this2 = this;
	
	            $.ajax({
	                url: '/api/users/my_account/',
	                dataType: 'json',
	                cache: false,
	                success: function success(data) {
	                    return _this2.setState({
	                        my_account: {
	                            id: data.id,
	                            username: data.username
	                        }
	                    });
	                },
	                error: function error(xhr, status, err) {
	                    return console.error(status, err.toString());
	                }
	            });
	        }
	    }, {
	        key: 'componentDidMount',
	        value: function componentDidMount() {
	            this.loadMyAccount();
	        }
	    }, {
	        key: 'render',
	        value: function render() {
	            var _this3 = this;
	
	            var MusicNodes = this.props.data.map(function (music, index) {
	                var level = _this3.props.is_srandom ? music.level.level : music.sran_level.level;
	                return _react2.default.createElement(_Music2.default, {
	                    key: index,
	                    id: music.id,
	                    title: music.title,
	                    level: level,
	                    difficulty: music.difficulty.difficulty_short,
	                    bpm: music.bpm,
	                    user: _this3.state.my_account
	                });
	            });
	
	            return _react2.default.createElement(
	                'table',
	                { className: 'music-list table table-condensed' },
	                _react2.default.createElement(
	                    'thead',
	                    null,
	                    _react2.default.createElement(
	                        'tr',
	                        null,
	                        _react2.default.createElement(
	                            'th',
	                            null,
	                            this.props.is_srandom ? 'Lv' : 'S乱Lv'
	                        ),
	                        _react2.default.createElement(
	                            'th',
	                            null,
	                            '\u66F2\u540D'
	                        ),
	                        _react2.default.createElement(
	                            'th',
	                            null,
	                            '\u96E3\u6613\u5EA6'
	                        ),
	                        _react2.default.createElement(
	                            'th',
	                            null,
	                            'BPM'
	                        ),
	                        _react2.default.createElement(
	                            'th',
	                            null,
	                            '\u30E1\u30C0\u30EB'
	                        ),
	                        _react2.default.createElement(
	                            'th',
	                            null,
	                            'BAD\u6570'
	                        ),
	                        _react2.default.createElement(
	                            'th',
	                            null,
	                            '\u66F4\u65B0\u65E5\u6642'
	                        )
	                    )
	                ),
	                _react2.default.createElement(
	                    'tbody',
	                    null,
	                    MusicNodes
	                )
	            );
	        }
	    }]);
	
	    return MusicTable;
	}(_react2.default.Component);
	
	exports.default = MusicTable;
	
	MusicTable.propTypes = {
	    data: _react2.default.PropTypes.array.isRequired,
	    count: _react2.default.PropTypes.number.isRequired,
	    is_srandom: _react2.default.PropTypes.bool.isRequired
	};
	MusicTable.defaultProps = {
	    data: [],
	    count: 0
	};

/***/ },

/***/ 174:
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }
	
	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }
	
	var Music = function (_React$Component) {
	    _inherits(Music, _React$Component);
	
	    function Music(props) {
	        _classCallCheck(this, Music);
	
	        var _this = _possibleConstructorReturn(this, (Music.__proto__ || Object.getPrototypeOf(Music)).call(this, props));
	
	        _this.state = {
	            record: {
	                medal: '-',
	                bad_count: '-',
	                updated_at: '-'
	            },
	            clear_status: 'no-play'
	        };
	        return _this;
	    }
	
	    _createClass(Music, [{
	        key: 'loadRecord',
	        value: function loadRecord() {
	            var _this2 = this;
	
	            $.ajax({
	                url: '/api/users/' + this.props.user.username + '/record/' + this.props.id + '/',
	                dataType: 'json',
	                cache: false,
	                success: function success(data) {
	                    var medal = data.medal.medal !== null ? data.medal.medal : '-';
	                    var bad_count = data.bad_count.bad_count !== null ? data.bad_count.bad_count : '-';
	                    var updated_at = data.medal.updated_at_jst !== null ? data.medal.updated_at_jst : '-';
	                    _this2.setState({
	                        record: {
	                            medal: medal,
	                            bad_count: bad_count,
	                            updated_at: updated_at
	                        }
	                    });
	                },
	                error: function error(xhr, status, err) {
	                    return console.error(status, err.toString());
	                }
	            });
	        }
	    }, {
	        key: 'loadClearStatus',
	        value: function loadClearStatus() {
	            var _this3 = this;
	
	            $.ajax({
	                url: '/api/get_clear_status/' + this.props.id + '/',
	                dataType: 'json',
	                cache: false,
	                success: function success(data) {
	                    return _this3.setState({ clear_status: data.clear_status });
	                },
	                error: function error(xhr, status, err) {
	                    return console.error(status, err.toString());
	                }
	            });
	        }
	    }, {
	        key: 'componentDidMount',
	        value: function componentDidMount() {
	            this.loadRecord();
	            this.loadClearStatus();
	        }
	    }, {
	        key: 'render',
	        value: function render() {
	            var _this4 = this;
	
	            var medal_img = function medal_img() {
	                return _this4.state.record.medal !== '-' && _this4.state.record.medal !== 12 ? _react2.default.createElement('img', { src: '/static/img/medal/' + _this4.state.record.medal + '.png', width: '16', height: '16' }) : '-';
	            };
	            return _react2.default.createElement(
	                'tr',
	                { id: 'music-' + this.props.id, className: this.state.clear_status },
	                _react2.default.createElement(
	                    'td',
	                    { className: 'level' },
	                    this.props.level
	                ),
	                _react2.default.createElement(
	                    'td',
	                    { className: 'title' },
	                    _react2.default.createElement(
	                        'a',
	                        { href: '/edit/' + this.props.id + '/' },
	                        this.props.title
	                    )
	                ),
	                _react2.default.createElement(
	                    'td',
	                    { className: 'difficulty' },
	                    this.props.difficulty
	                ),
	                _react2.default.createElement(
	                    'td',
	                    { className: 'bpm' },
	                    this.props.bpm
	                ),
	                _react2.default.createElement(
	                    'td',
	                    { className: 'medal' },
	                    medal_img()
	                ),
	                _react2.default.createElement(
	                    'td',
	                    { className: 'bad_count' },
	                    this.state.record.bad_count
	                ),
	                _react2.default.createElement(
	                    'td',
	                    { className: 'updated_at' },
	                    this.state.record.updated_at
	                )
	            );
	        }
	    }]);
	
	    return Music;
	}(_react2.default.Component);
	
	exports.default = Music;
	
	Music.propTypes = {
	    id: _react2.default.PropTypes.number.isRequired,
	    title: _react2.default.PropTypes.string.isRequired,
	    level: _react2.default.PropTypes.number.isRequired,
	    difficulty: _react2.default.PropTypes.string.isRequired,
	    bpm: _react2.default.PropTypes.string.isRequired,
	    user: _react2.default.PropTypes.object.isRequired
	};

/***/ },

/***/ 175:
/***/ function(module, exports, __webpack_require__) {

	"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	var _react = __webpack_require__(1);
	
	var _react2 = _interopRequireDefault(_react);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }
	
	function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }
	
	/* ローディング中のアニメーション */
	var Loader = function (_React$Component) {
	    _inherits(Loader, _React$Component);
	
	    function Loader() {
	        _classCallCheck(this, Loader);
	
	        return _possibleConstructorReturn(this, (Loader.__proto__ || Object.getPrototypeOf(Loader)).apply(this, arguments));
	    }
	
	    _createClass(Loader, [{
	        key: "render",
	        value: function render() {
	            if (this.props.is_active) {
	                return _react2.default.createElement(
	                    "div",
	                    { id: "loader", style: { textAlign: "center" } },
	                    _react2.default.createElement("i", { className: "fa fa-refresh fa-spin fa-3x" })
	                );
	            } else {
	                return null;
	            }
	        }
	    }]);
	
	    return Loader;
	}(_react2.default.Component);
	
	exports.default = Loader;
	
	Loader.propTypes = { is_active: _react2.default.PropTypes.bool.isRequired };

/***/ }

});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9zdGF0aWMvcmVhY3Qvc3JjL2RpZmZsaXN0LmpzeCIsIndlYnBhY2s6Ly8vLi9zdGF0aWMvcmVhY3Qvc3JjL2NvbXBvbmVudHMvTXVzaWNMaXN0LmpzeCIsIndlYnBhY2s6Ly8vLi9zdGF0aWMvcmVhY3Qvc3JjL2NvbXBvbmVudHMvTXVzaWNUYWJsZS5qc3giLCJ3ZWJwYWNrOi8vLy4vc3RhdGljL3JlYWN0L3NyYy9jb21wb25lbnRzL011c2ljLmpzeCIsIndlYnBhY2s6Ly8vLi9zdGF0aWMvcmVhY3Qvc3JjL2NvbXBvbmVudHMvTG9hZGVyLmpzeCJdLCJuYW1lcyI6WyJ1cmwiLCJ3aW5kb3ciLCJsb2NhdGlvbiIsImhyZWYiLCJzcGxpdF91cmwiLCJzcGxpdCIsImlzX3NyYW5kb20iLCJsZXZlbCIsIk51bWJlciIsInJlbmRlciIsImRvY3VtZW50IiwiZ2V0RWxlbWVudEJ5SWQiLCJNdXNpY0xpc3QiLCJwcm9wcyIsInN0YXRlIiwiZGF0YSIsImZvbGRlcl9sYW1wIiwibG9hZGluZyIsIm1heF9sdiIsImx2IiwiJCIsImFqYXgiLCJkYXRhVHlwZSIsImNhY2hlIiwic3VjY2VzcyIsInNldFN0YXRlIiwiZXJyb3IiLCJ4aHIiLCJzdGF0dXMiLCJlcnIiLCJjb25zb2xlIiwidG9TdHJpbmciLCJsb2FkTXVzaWNMaXN0IiwibG9hZEZvbGRlckxhbXAiLCJyZXN1bHRzIiwiY291bnQiLCJDb21wb25lbnQiLCJwcm9wVHlwZXMiLCJQcm9wVHlwZXMiLCJudW1iZXIiLCJpc1JlcXVpcmVkIiwiYm9vbCIsIk11c2ljVGFibGUiLCJteV9hY2NvdW50IiwiaWQiLCJ1c2VybmFtZSIsImxvYWRNeUFjY291bnQiLCJNdXNpY05vZGVzIiwibWFwIiwibXVzaWMiLCJpbmRleCIsInNyYW5fbGV2ZWwiLCJ0aXRsZSIsImRpZmZpY3VsdHkiLCJkaWZmaWN1bHR5X3Nob3J0IiwiYnBtIiwiYXJyYXkiLCJkZWZhdWx0UHJvcHMiLCJNdXNpYyIsInJlY29yZCIsIm1lZGFsIiwiYmFkX2NvdW50IiwidXBkYXRlZF9hdCIsImNsZWFyX3N0YXR1cyIsInVzZXIiLCJ1cGRhdGVkX2F0X2pzdCIsImxvYWRSZWNvcmQiLCJsb2FkQ2xlYXJTdGF0dXMiLCJtZWRhbF9pbWciLCJzdHJpbmciLCJvYmplY3QiLCJMb2FkZXIiLCJpc19hY3RpdmUiLCJ0ZXh0QWxpZ24iXSwibWFwcGluZ3MiOiI7Ozs7Ozs7QUFBQTs7OztBQUNBOzs7O0FBQ0E7Ozs7OztBQUVBO0FBQ0EsS0FBTUEsTUFBTUMsT0FBT0MsUUFBUCxDQUFnQkMsSUFBNUI7QUFDQSxLQUFNQyxZQUFZSixJQUFJSyxLQUFKLENBQVUsR0FBVixDQUFsQjtBQUNBLEtBQU1DLGFBQWFGLFVBQVUsQ0FBVixNQUFpQixVQUFwQztBQUNBLEtBQU1HLFFBQVFDLE9BQU9KLFVBQVUsQ0FBVixDQUFQLENBQWQ7O0FBRUE7QUFDQSxvQkFBU0ssTUFBVCxDQUNJLHFEQUFXLElBQUlGLEtBQWYsRUFBc0IsWUFBWUQsVUFBbEMsR0FESixFQUVJSSxTQUFTQyxjQUFULENBQXdCLFNBQXhCLENBRkosRTs7Ozs7Ozs7Ozs7Ozs7O0FDWEE7Ozs7QUFDQTs7OztBQUNBOzs7Ozs7Ozs7Ozs7S0FFcUJDLFM7OztBQUNqQix3QkFBWUMsS0FBWixFQUFtQjtBQUFBOztBQUFBLDJIQUNUQSxLQURTOztBQUVmLGVBQUtDLEtBQUwsR0FBYTtBQUNUQyxtQkFBTSxFQURHO0FBRVRDLDBCQUFhLFNBRko7QUFHVEMsc0JBQVM7QUFIQSxVQUFiO0FBRmU7QUFPbEI7Ozs7eUNBRWU7QUFBQTs7QUFDWixpQkFBTUMsU0FBUyxLQUFLTCxLQUFMLENBQVdQLFVBQVgsR0FBd0IsRUFBeEIsR0FBNkIsRUFBNUM7QUFDQSxpQkFBTU4sTUFBTSxLQUFLYSxLQUFMLENBQVdQLFVBQVgsZ0NBQWtEWSxTQUFPLENBQVAsR0FBUyxLQUFLTCxLQUFMLENBQVdNLEVBQXRFLHNEQUF1SEQsU0FBTyxDQUFQLEdBQVMsS0FBS0wsS0FBTCxDQUFXTSxFQUEzSSxnQ0FBWjtB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QkFBWSxnQkFBTWYsU0FBTixDQUFnQitCLE1BQWhCLENBQXVCN0IsVUFKckI7QUFLZGUsVUFBSyxnQkFBTWpCLFNBQU4sQ0FBZ0IrQixNQUFoQixDQUF1QjdCLFVBTGQ7QUFNZHdCLFdBQU0sZ0JBQU0xQixTQUFOLENBQWdCZ0MsTUFBaEIsQ0FBdUI5QjtBQU5mLEVBQWxCLEM7Ozs7Ozs7Ozs7Ozs7OztBQ2xFQTs7Ozs7Ozs7Ozs7O0FBRUE7S0FDcUIrQixNOzs7Ozs7Ozs7OztrQ0FDUjtBQUNMLGlCQUFJLEtBQUsxRCxLQUFMLENBQVcyRCxTQUFmLEVBQTBCO0FBQ3RCLHdCQUNJO0FBQUE7QUFBQSx1QkFBSyxJQUFHLFFBQVIsRUFBaUIsT0FBTyxFQUFDQyxXQUFXLFFBQVosRUFBeEI7QUFDSSwwREFBRyxXQUFVLDZCQUFiO0FBREosa0JBREo7QUFLSCxjQU5ELE1BTU87QUFDSCx3QkFBTyxJQUFQO0FBQ0g7QUFDSjs7OztHQVgrQixnQkFBTXJDLFM7O21CQUFyQm1DLE07O0FBYXJCQSxRQUFPbEMsU0FBUCxHQUFtQixFQUFFbUMsV0FBVyxnQkFBTWxDLFNBQU4sQ0FBZ0JHLElBQWhCLENBQXFCRCxVQUFsQyxFQUFuQixDIiwiZmlsZSI6ImRpZmZsaXN0LmpzIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IE11c2ljTGlzdCBmcm9tICcuL2NvbXBvbmVudHMvTXVzaWNMaXN0JztcblxuLy8gVVJM44GL44KJ6Zuj5piT5bqm6KGo44Go44Os44OZ44Or44KS5Yik5a6aXG5jb25zdCB1cmwgPSB3aW5kb3cubG9jYXRpb24uaHJlZjtcbmNvbnN0IHNwbGl0X3VybCA9IHVybC5zcGxpdCgnLycpO1xuY29uc3QgaXNfc3JhbmRvbSA9IHNwbGl0X3VybFszXSA9PT0gJ2RpZmZsaXN0JztcbmNvbnN0IGxldmVsID0gTnVtYmVyKHNwbGl0X3VybFs0XSk7XG5cbi8vIFRPRE86IOiomOmMsue3qOmbhuapn+iDveOCkuWun+ijhVxuUmVhY3RET00ucmVuZGVyKFxuICAgIDxNdXNpY0xpc3QgbHY9e2xldmVsfSBpc19zcmFuZG9tPXtpc19zcmFuZG9tfSAvPixcbiAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnY29udGVudCcpXG4pO1xuXG5cblxuLy8gV0VCUEFDSyBGT09URVIgLy9cbi8vIC4vc3RhdGljL3JlYWN0L3NyYy9kaWZmbGlzdC5qc3giLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IE11c2ljVGFibGUgZnJvbSAnLi9NdXNpY1RhYmxlJztcbmltcG9ydCBMb2FkZXIgZnJvbSAnLi9Mb2FkZXInO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBNdXNpY0xpc3QgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIGRhdGE6IFtdLFxuICAgICAgICAgICAgZm9sZGVyX2xhbXA6ICduby1wbGF5JyxcbiAgICAgICAgICAgIGxvYWRpbmc6IHRydWVcbiAgICAgICAgfTtcbiAgICB9XG5cbiAgICBsb2FkTXVzaWNMaXN0KCkge1xuICAgICAgICBjb25zdCBtYXhfbHYgPSB0aGlzLnByb3BzLmlzX3NyYW5kb20gPyAxNyA6IDUwO1xuICAgICAgICBjb25zdCB1cmwgPSB0aGlzLnByb3BzLmlzX3NyYW5kb20gPyBgL2FwaS9tdXNpYy8/c3Jhbl9sZXZlbD0ke21heF9sdisxLXRoaXMucHJvcHMubHZ9Jm9yZGVyaW5nPWxldmVsLHRpdGxlYCA6IGAvYXBpL211c2ljLz9sZXZlbD0ke21heF9sdisxLXRoaXMucHJvcHMubHZ9Jm9yZGVyaW5nPXNyYW5fbGV2ZWwsdGl0bGVgO1xuICAgICAgICAkLmFqYXgoe1xuICAgICAgICAgICAgdXJsOiB1cmwsXG4gICAgICAgICAgICBkYXRhVHlwZTogJ2pzb24nLFxuICAgICAgICAgICAgY2FjaGU6IGZhbHNlLFxuICAgICAgICAgICAgc3VjY2VzczogZGF0YSA9PiB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgICAgICAgICBkYXRhOiBkYXRhLFxuICAgICAgICAgICAgICAgIGxvYWRpbmc6IGZhbHNlXG4gICAgICAgICAgICB9KSxcbiAgICAgICAgICAgIGVycm9yOiAoeGhyLCBzdGF0dXMsIGVycikgPT4gY29uc29sZS5lcnJvcihzdGF0dXMsIGVyci50b1N0cmluZygpKVxuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBsb2FkRm9sZGVyTGFtcCgpIHtcbiAgICAgICAgJC5hamF4KHtcbiAgICAgICAgICAgIHVybDogYC9hcGkvZ2V0X2ZvbGRlcl9sYW1wLyR7dGhpcy5wcm9wcy5sdn0vYCxcbiAgICAgICAgICAgIGRhdGFUeXBlOiAnanNvbicsXG4gICAgICAgICAgICBkYXRhOiB7aXNfc3JhbmRvbTogdGhpcy5wcm9wcy5pc19zcmFuZG9tfSxcbiAgICAgICAgICAgIGNhY2hlOiBmYWxzZSxcbiAgICAgICAgICAgIHN1Y2Nlc3M6IGRhdGEgPT4gdGhpcy5zZXRTdGF0ZSh7IGZvbGRlcl9sYW1wOiBkYXRhLmZvbGRlcl9sYW1wIH0pLFxuICAgICAgICAgICAgZXJyb3I6ICh4aHIsIHN0YXR1cywgZXJyKSA9PiBjb25zb2xlLmVycm9yKHN0YXR1cywgZXJyLnRvU3RyaW5nKCkpXG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgICAgICB0aGlzLmxvYWRNdXNpY0xpc3QoKTtcbiAgICAgICAgdGhpcy5sb2FkRm9sZGVyTGFtcCgpO1xuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYgaWQ9XCJtdXNpYy1saXN0XCI+XG4gICAgICAgICAgICAgICAgPGgzIGlkPXtgbHYke3RoaXMucHJvcHMubHZ9YH0gY2xhc3NOYW1lPXtgbGV2ZWwtZm9sZGVyICR7dGhpcy5zdGF0ZS5mb2xkZXJfbGFtcH1gfT5Mdnt0aGlzLnByb3BzLmx2fTwvaDM+XG4gICAgICAgICAgICAgICAgPE11c2ljVGFibGUgZGF0YT17dGhpcy5zdGF0ZS5kYXRhLnJlc3VsdHN9IGNvdW50PXt0aGlzLnN0YXRlLmRhdGEuY291bnR9IGlzX3NyYW5kb209e3RoaXMucHJvcHMuaXNfc3JhbmRvbX0gLz5cbiAgICAgICAgICAgICAgICA8TG9hZGVyIGlzX2FjdGl2ZT17dGhpcy5zdGF0ZS5sb2FkaW5nfSAvPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuTXVzaWNMaXN0LnByb3BUeXBlcyA9IHtcbiAgICBsdjogUmVhY3QuUHJvcFR5cGVzLm51bWJlci5pc1JlcXVpcmVkLFxuICAgIGlzX3NyYW5kb206IFJlYWN0LlByb3BUeXBlcy5ib29sLmlzUmVxdWlyZWRcbn07XG5cblxuXG4vLyBXRUJQQUNLIEZPT1RFUiAvL1xuLy8gLi9zdGF0aWMvcmVhY3Qvc3JjL2NvbXBvbmVudHMvTXVzaWNMaXN0LmpzeCIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgTXVzaWMgZnJvbSAnLi9NdXNpYyc7XG5cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIE11c2ljVGFibGUgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIG15X2FjY291bnQ6IHtcbiAgICAgICAgICAgICAgICBpZDogJycsXG4gICAgICAgICAgICAgICAgdXNlcm5hbWU6ICcnXG4gICAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgfVxuXG4gICAgbG9hZE15QWNjb3VudCgpIHtcbiAgICAgICAgJC5hamF4KHtcbiAgICAgICAgICAgIHVybDogJy9hcGkvdXNlcnMvbXlfYWNjb3VudC8nLFxuICAgICAgICAgICAgZGF0YVR5cGU6ICdqc29uJyxcbiAgICAgICAgICAgIGNhY2hlOiBmYWxzZSxcbiAgICAgICAgICAgIHN1Y2Nlc3M6IGRhdGEgPT4gdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgICAgICAgbXlfYWNjb3VudDoge1xuICAgICAgICAgICAgICAgICAgICBpZDogZGF0YS5pZCxcbiAgICAgICAgICAgICAgICAgICAgdXNlcm5hbWU6IGRhdGEudXNlcm5hbWVcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9KSxcbiAgICAgICAgICAgIGVycm9yOiAoeGhyLCBzdGF0dXMsIGVycikgPT4gY29uc29sZS5lcnJvcihzdGF0dXMsIGVyci50b1N0cmluZygpKVxuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICAgICAgdGhpcy5sb2FkTXlBY2NvdW50KCk7XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCBNdXNpY05vZGVzID0gdGhpcy5wcm9wcy5kYXRhLm1hcCgobXVzaWMsIGluZGV4KSA9PiB7XG4gICAgICAgICAgICBjb25zdCBsZXZlbCA9IHRoaXMucHJvcHMuaXNfc3JhbmRvbSA/IG11c2ljLmxldmVsLmxldmVsIDogbXVzaWMuc3Jhbl9sZXZlbC5sZXZlbDtcbiAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgPE11c2ljXG4gICAgICAgICAgICAgICAgICAgIGtleT17aW5kZXh9XG4gICAgICAgICAgICAgICAgICAgIGlkPXttdXNpYy5pZH1cbiAgICAgICAgICAgICAgICAgICAgdGl0bGU9e211c2ljLnRpdGxlfVxuICAgICAgICAgICAgICAgICAgICBsZXZlbD17bGV2ZWx9XG4gICAgICAgICAgICAgICAgICAgIGRpZmZpY3VsdHk9e211c2ljLmRpZmZpY3VsdHkuZGlmZmljdWx0eV9zaG9ydH1cbiAgICAgICAgICAgICAgICAgICAgYnBtPXttdXNpYy5icG19XG4gICAgICAgICAgICAgICAgICAgIHVzZXI9e3RoaXMuc3RhdGUubXlfYWNjb3VudH1cbiAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDx0YWJsZSBjbGFzc05hbWU9XCJtdXNpYy1saXN0IHRhYmxlIHRhYmxlLWNvbmRlbnNlZFwiPlxuICAgICAgICAgICAgICAgIDx0aGVhZD5cbiAgICAgICAgICAgICAgICAgICAgPHRyPlxuICAgICAgICAgICAgICAgICAgICAgICAgPHRoPnt0aGlzLnByb3BzLmlzX3NyYW5kb20gPyAnTHYnIDogJ1PkubFMdid9PC90aD5cbiAgICAgICAgICAgICAgICAgICAgICAgIDx0aD7mm7LlkI08L3RoPlxuICAgICAgICAgICAgICAgICAgICAgICAgPHRoPumbo+aYk+W6pjwvdGg+XG4gICAgICAgICAgICAgICAgICAgICAgICA8dGg+QlBNPC90aD5cbiAgICAgICAgICAgICAgICAgICAgICAgIDx0aD7jg6Hjg4Djg6s8L3RoPlxuICAgICAgICAgICAgICAgICAgICAgICAgPHRoPkJBROaVsDwvdGg+XG4gICAgICAgICAgICAgICAgICAgICAgICA8dGg+5pu05paw5pel5pmCPC90aD5cbiAgICAgICAgICAgICAgICAgICAgPC90cj5cbiAgICAgICAgICAgICAgICA8L3RoZWFkPlxuICAgICAgICAgICAgICAgIDx0Ym9keT5cbiAgICAgICAgICAgICAgICAgICAge011c2ljTm9kZXN9XG4gICAgICAgICAgICAgICAgPC90Ym9keT5cbiAgICAgICAgICAgIDwvdGFibGU+XG4gICAgICAgICk7XG4gICAgfVxufVxuTXVzaWNUYWJsZS5wcm9wVHlwZXMgPSB7XG4gICAgZGF0YTogUmVhY3QuUHJvcFR5cGVzLmFycmF5LmlzUmVxdWlyZWQsXG4gICAgY291bnQ6IFJlYWN0LlByb3BUeXBlcy5udW1iZXIuaXNSZXF1aXJlZCxcbiAgICBpc19zcmFuZG9tOiBSZWFjdC5Qcm9wVHlwZXMuYm9vbC5pc1JlcXVpcmVkXG59O1xuTXVzaWNUYWJsZS5kZWZhdWx0UHJvcHMgPSB7XG4gICAgZGF0YTogW10sXG4gICAgY291bnQ6IDBcbn07XG5cblxuXG4vLyBXRUJQQUNLIEZPT1RFUiAvL1xuLy8gLi9zdGF0aWMvcmVhY3Qvc3JjL2NvbXBvbmVudHMvTXVzaWNUYWJsZS5qc3giLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBNdXNpYyBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgcmVjb3JkOiB7XG4gICAgICAgICAgICAgICAgbWVkYWw6ICctJyxcbiAgICAgICAgICAgICAgICBiYWRfY291bnQ6ICctJyxcbiAgICAgICAgICAgICAgICB1cGRhdGVkX2F0OiAnLSdcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBjbGVhcl9zdGF0dXM6ICduby1wbGF5J1xuICAgICAgICB9O1xuICAgIH1cblxuICAgIGxvYWRSZWNvcmQoKSB7XG4gICAgICAgICQuYWpheCh7XG4gICAgICAgICAgICB1cmw6IGAvYXBpL3VzZXJzLyR7dGhpcy5wcm9wcy51c2VyLnVzZXJuYW1lfS9yZWNvcmQvJHt0aGlzLnByb3BzLmlkfS9gLFxuICAgICAgICAgICAgZGF0YVR5cGU6ICdqc29uJyxcbiAgICAgICAgICAgIGNhY2hlOiBmYWxzZSxcbiAgICAgICAgICAgIHN1Y2Nlc3M6IGRhdGEgPT4ge1xuICAgICAgICAgICAgICAgIGNvbnN0IG1lZGFsID0gZGF0YS5tZWRhbC5tZWRhbCAhPT0gbnVsbCA/IGRhdGEubWVkYWwubWVkYWwgOiAnLSc7XG4gICAgICAgICAgICAgICAgY29uc3QgYmFkX2NvdW50ID0gZGF0YS5iYWRfY291bnQuYmFkX2NvdW50ICE9PSBudWxsID8gZGF0YS5iYWRfY291bnQuYmFkX2NvdW50IDogJy0nO1xuICAgICAgICAgICAgICAgIGNvbnN0IHVwZGF0ZWRfYXQgPSBkYXRhLm1lZGFsLnVwZGF0ZWRfYXRfanN0ICE9PSBudWxsID8gZGF0YS5tZWRhbC51cGRhdGVkX2F0X2pzdCA6ICctJztcbiAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgICAgICAgICAgICAgcmVjb3JkOiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBtZWRhbDogbWVkYWwsXG4gICAgICAgICAgICAgICAgICAgICAgICBiYWRfY291bnQ6IGJhZF9jb3VudCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHVwZGF0ZWRfYXQ6IHVwZGF0ZWRfYXRcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIGVycm9yOiAoeGhyLCBzdGF0dXMsIGVycikgPT4gY29uc29sZS5lcnJvcihzdGF0dXMsIGVyci50b1N0cmluZygpKVxuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBsb2FkQ2xlYXJTdGF0dXMoKSB7XG4gICAgICAgICQuYWpheCh7XG4gICAgICAgICAgICB1cmw6IGAvYXBpL2dldF9jbGVhcl9zdGF0dXMvJHt0aGlzLnByb3BzLmlkfS9gLFxuICAgICAgICAgICAgZGF0YVR5cGU6ICdqc29uJyxcbiAgICAgICAgICAgIGNhY2hlOiBmYWxzZSxcbiAgICAgICAgICAgIHN1Y2Nlc3M6IGRhdGEgPT4gdGhpcy5zZXRTdGF0ZSh7IGNsZWFyX3N0YXR1czogZGF0YS5jbGVhcl9zdGF0dXMgfSksXG4gICAgICAgICAgICBlcnJvcjogKHhociwgc3RhdHVzLCBlcnIpID0+IGNvbnNvbGUuZXJyb3Ioc3RhdHVzLCBlcnIudG9TdHJpbmcoKSlcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgICAgIHRoaXMubG9hZFJlY29yZCgpO1xuICAgICAgICB0aGlzLmxvYWRDbGVhclN0YXR1cygpO1xuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3QgbWVkYWxfaW1nID0gKCkgPT4gKHRoaXMuc3RhdGUucmVjb3JkLm1lZGFsICE9PSAnLScgJiYgdGhpcy5zdGF0ZS5yZWNvcmQubWVkYWwgIT09IDEyKSA/IDxpbWcgc3JjPXtgL3N0YXRpYy9pbWcvbWVkYWwvJHt0aGlzLnN0YXRlLnJlY29yZC5tZWRhbH0ucG5nYH0gd2lkdGg9XCIxNlwiIGhlaWdodD1cIjE2XCIgLz4gOiAnLSdcbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDx0ciBpZD17YG11c2ljLSR7dGhpcy5wcm9wcy5pZH1gfSBjbGFzc05hbWU9e3RoaXMuc3RhdGUuY2xlYXJfc3RhdHVzfT5cbiAgICAgICAgICAgICAgICA8dGQgY2xhc3NOYW1lPVwibGV2ZWxcIj57dGhpcy5wcm9wcy5sZXZlbH08L3RkPlxuICAgICAgICAgICAgICAgIDx0ZCBjbGFzc05hbWU9XCJ0aXRsZVwiPjxhIGhyZWY9e2AvZWRpdC8ke3RoaXMucHJvcHMuaWR9L2B9Pnt0aGlzLnByb3BzLnRpdGxlfTwvYT48L3RkPlxuICAgICAgICAgICAgICAgIDx0ZCBjbGFzc05hbWU9XCJkaWZmaWN1bHR5XCI+e3RoaXMucHJvcHMuZGlmZmljdWx0eX08L3RkPlxuICAgICAgICAgICAgICAgIDx0ZCBjbGFzc05hbWU9XCJicG1cIj57dGhpcy5wcm9wcy5icG19PC90ZD5cbiAgICAgICAgICAgICAgICA8dGQgY2xhc3NOYW1lPVwibWVkYWxcIj57bWVkYWxfaW1nKCl9PC90ZD5cbiAgICAgICAgICAgICAgICA8dGQgY2xhc3NOYW1lPVwiYmFkX2NvdW50XCI+e3RoaXMuc3RhdGUucmVjb3JkLmJhZF9jb3VudH08L3RkPlxuICAgICAgICAgICAgICAgIDx0ZCBjbGFzc05hbWU9XCJ1cGRhdGVkX2F0XCI+e3RoaXMuc3RhdGUucmVjb3JkLnVwZGF0ZWRfYXR9PC90ZD5cbiAgICAgICAgICAgIDwvdHI+XG4gICAgICAgICk7XG4gICAgfVxufVxuTXVzaWMucHJvcFR5cGVzID0ge1xuICAgIGlkOiBSZWFjdC5Qcm9wVHlwZXMubnVtYmVyLmlzUmVxdWlyZWQsXG4gICAgdGl0bGU6IFJlYWN0LlByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBsZXZlbDogUmVhY3QuUHJvcFR5cGVzLm51bWJlci5pc1JlcXVpcmVkLFxuICAgIGRpZmZpY3VsdHk6IFJlYWN0LlByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBicG06IFJlYWN0LlByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICB1c2VyOiBSZWFjdC5Qcm9wVHlwZXMub2JqZWN0LmlzUmVxdWlyZWRcbn07XG5cblxuXG4vLyBXRUJQQUNLIEZPT1RFUiAvL1xuLy8gLi9zdGF0aWMvcmVhY3Qvc3JjL2NvbXBvbmVudHMvTXVzaWMuanN4IiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyog44Ot44O844OH44Kj44Oz44Kw5Lit44Gu44Ki44OL44Oh44O844K344On44OzICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBMb2FkZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIHJlbmRlcigpIHtcbiAgICAgICAgaWYgKHRoaXMucHJvcHMuaXNfYWN0aXZlKSB7XG4gICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgIDxkaXYgaWQ9XCJsb2FkZXJcIiBzdHlsZT17e3RleHRBbGlnbjogXCJjZW50ZXJcIn19PlxuICAgICAgICAgICAgICAgICAgICA8aSBjbGFzc05hbWU9XCJmYSBmYS1yZWZyZXNoIGZhLXNwaW4gZmEtM3hcIj48L2k+XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICApXG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICByZXR1cm4gbnVsbDtcbiAgICAgICAgfVxuICAgIH1cbn1cbkxvYWRlci5wcm9wVHlwZXMgPSB7IGlzX2FjdGl2ZTogUmVhY3QuUHJvcFR5cGVzLmJvb2wuaXNSZXF1aXJlZCB9O1xuXG5cblxuLy8gV0VCUEFDSyBGT09URVIgLy9cbi8vIC4vc3RhdGljL3JlYWN0L3NyYy9jb21wb25lbnRzL0xvYWRlci5qc3giXSwic291cmNlUm9vdCI6IiJ9