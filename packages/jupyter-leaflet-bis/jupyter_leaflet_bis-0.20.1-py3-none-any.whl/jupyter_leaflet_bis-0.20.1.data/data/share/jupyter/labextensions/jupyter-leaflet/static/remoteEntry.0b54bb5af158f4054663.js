var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ 7536:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e(82), __webpack_require__.e(279), __webpack_require__.e(672), __webpack_require__.e(488), __webpack_require__.e(330)]).then(() => (() => ((__webpack_require__(3553)))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e(488), __webpack_require__.e(869)]).then(() => (() => ((__webpack_require__(1869)))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/amd options */
/******/ 	(() => {
/******/ 		__webpack_require__.amdO = {};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"10":"1136e4ec9cc1b4c55d9c","82":"7ec38a4a4a3b81084e97","94":"fa60b264c60c21c3912a","142":"f3aef6f68bf9ede38ed0","176":"1164b8a44947bcd1ec86","180":"854f60c8647f2e0e0a5a","189":"8f65799691d51f140703","256":"a858b7c7e3fe25bb503f","268":"6a18bae826d6df03ad6c","269":"d7fc4b6fa64e6c228779","320":"53805359fe1724ade379","330":"568ba39e1bf93cf13ea9","363":"29af6f5877353fa868de","380":"0670b1dd52b658ae21c6","389":"b60987a4170fd2498ba6","464":"7d59c126d40beb0d0313","512":"754f85977f7520c3a106","577":"45ca93eba1359b8fe87c","630":"8d23435aae8754c924a0","672":"b51401254da31b8a670a","761":"e76830aec9958099f110","844":"f5cfec3076837aaaf4a0","862":"50b6d5106e3a895d3a5c","869":"b2df99816553e17faf35","939":"b2048b7fa57b6bc9cff4","958":"c741a8fca5ac6d97f8e4"}[chunkId] + ".js?v=" + {"10":"1136e4ec9cc1b4c55d9c","82":"7ec38a4a4a3b81084e97","94":"fa60b264c60c21c3912a","142":"f3aef6f68bf9ede38ed0","176":"1164b8a44947bcd1ec86","180":"854f60c8647f2e0e0a5a","189":"8f65799691d51f140703","256":"a858b7c7e3fe25bb503f","268":"6a18bae826d6df03ad6c","269":"d7fc4b6fa64e6c228779","320":"53805359fe1724ade379","330":"568ba39e1bf93cf13ea9","363":"29af6f5877353fa868de","380":"0670b1dd52b658ae21c6","389":"b60987a4170fd2498ba6","464":"7d59c126d40beb0d0313","512":"754f85977f7520c3a106","577":"45ca93eba1359b8fe87c","630":"8d23435aae8754c924a0","672":"b51401254da31b8a670a","761":"e76830aec9958099f110","844":"f5cfec3076837aaaf4a0","862":"50b6d5106e3a895d3a5c","869":"b2df99816553e17faf35","939":"b2048b7fa57b6bc9cff4","958":"c741a8fca5ac6d97f8e4"}[chunkId] + "";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "jupyter-leaflet-bis:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 		
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => {
/******/ 				if (typeof console !== "undefined" && console.warn) console.warn(msg);
/******/ 			};
/******/ 			var uniqueName = "jupyter-leaflet-bis";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("@geoman-io/leaflet-geoman-free", "2.18.3", () => (__webpack_require__.e(10).then(() => (() => (__webpack_require__(5010))))));
/******/ 					register("jupyter-leaflet-bis", "0.20.1", () => (Promise.all([__webpack_require__.e(82), __webpack_require__.e(279), __webpack_require__.e(672), __webpack_require__.e(488), __webpack_require__.e(330)]).then(() => (() => (__webpack_require__(3553))))));
/******/ 					register("leaflet-ant-path", "1.3.0", () => (Promise.all([__webpack_require__.e(512), __webpack_require__.e(224)]).then(() => (() => (__webpack_require__(2512))))));
/******/ 					register("leaflet-defaulticon-compatibility", "0.1.2", () => (Promise.all([__webpack_require__.e(279), __webpack_require__.e(939)]).then(() => (() => (__webpack_require__(939))))));
/******/ 					register("leaflet-draw", "1.0.4", () => (__webpack_require__.e(269).then(() => (() => (__webpack_require__(6269))))));
/******/ 					register("leaflet-fullscreen", "1.0.2", () => (__webpack_require__.e(189).then(() => (() => (__webpack_require__(2189))))));
/******/ 					register("leaflet-measure", "3.1.0", () => (__webpack_require__.e(380).then(() => (() => (__webpack_require__(380))))));
/******/ 					register("leaflet-rotatedmarker", "0.2.0", () => (__webpack_require__.e(180).then(() => (() => (__webpack_require__(1180))))));
/******/ 					register("leaflet-search", "2.9.8", () => (Promise.all([__webpack_require__.e(844), __webpack_require__.e(104)]).then(() => (() => (__webpack_require__(9844))))));
/******/ 					register("leaflet-splitmap", "1.0.3", () => (Promise.all([__webpack_require__.e(35), __webpack_require__.e(958)]).then(() => (() => (__webpack_require__(6958))))));
/******/ 					register("leaflet-transform", "1.0.3", () => (Promise.all([__webpack_require__.e(94), __webpack_require__.e(35)]).then(() => (() => (__webpack_require__(2094))))));
/******/ 					register("leaflet-velocity", "1.9.2", () => (__webpack_require__.e(464).then(() => (() => (__webpack_require__(2464))))));
/******/ 					register("leaflet.awesome-markers", "2.0.5", () => (__webpack_require__.e(268).then(() => (() => (__webpack_require__(4268))))));
/******/ 					register("leaflet.markercluster", "1.5.3", () => (__webpack_require__.e(389).then(() => (() => (__webpack_require__(9389))))));
/******/ 					register("leaflet.vectorgrid", "1.3.0", () => (__webpack_require__.e(256).then(() => (() => (__webpack_require__(4256))))));
/******/ 					register("leaflet", "1.9.4", () => (__webpack_require__.e(862).then(() => (() => (__webpack_require__(3481))))));
/******/ 					register("proj4", "2.15.0", () => (__webpack_require__.e(363).then(() => (() => (__webpack_require__(363))))));
/******/ 					register("proj4leaflet", "1.0.2", () => (Promise.all([__webpack_require__.e(279), __webpack_require__.e(481), __webpack_require__.e(142)]).then(() => (() => (__webpack_require__(7142))))));
/******/ 					register("protomaps-leaflet", "1.24.2", () => (__webpack_require__.e(630).then(() => (() => (__webpack_require__(2630))))));
/******/ 					register("spin.js", "4.1.2", () => (__webpack_require__.e(176).then(() => (() => (__webpack_require__(6176))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript && document.currentScript.tagName.toUpperCase() === 'SCRIPT')
/******/ 				scriptUrl = document.currentScript.src;
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) {
/******/ 					var i = scripts.length - 1;
/******/ 					while (i > -1 && (!scriptUrl || !/^http(s?):/.test(scriptUrl))) scriptUrl = scripts[i--].src;
/******/ 				}
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/^blob:/, "").replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var exists = (scope, key) => {
/******/ 			return scope && __webpack_require__.o(scope, key);
/******/ 		}
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var eagerOnly = (versions) => {
/******/ 			return Object.keys(versions).reduce((filtered, version) => {
/******/ 					if (versions[version].eager) {
/******/ 						filtered[version] = versions[version];
/******/ 					}
/******/ 					return filtered;
/******/ 			}, {});
/******/ 		};
/******/ 		var findLatestVersion = (scope, key, eager) => {
/******/ 			var versions = eager ? eagerOnly(scope[key]) : scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key];
/******/ 		};
/******/ 		var findSatisfyingVersion = (scope, key, requiredVersion, eager) => {
/******/ 			var versions = eager ? eagerOnly(scope[key]) : scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key, eager) => {
/******/ 			var versions = eager ? eagerOnly(scope[key]) : scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion, eager) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ")" + (eager ? " for eager consumption" : "") + " of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var fail = (msg) => {
/******/ 			throw new Error(msg);
/******/ 		}
/******/ 		var failAsNotExist = (scopeName, key) => {
/******/ 			return fail("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 		}
/******/ 		var warn = /*#__PURE__*/ (msg) => {
/******/ 			if (typeof console !== "undefined" && console.warn) console.warn(msg);
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, key, eager, c, d) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then && !eager) {
/******/ 				return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], key, false, c, d));
/******/ 			}
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], key, eager, c, d);
/******/ 		});
/******/ 		
/******/ 		var useFallback = (scopeName, key, fallback) => {
/******/ 			return fallback ? fallback() : failAsNotExist(scopeName, key);
/******/ 		}
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key, eager, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			return get(findLatestVersion(scope, key, eager));
/******/ 		});
/******/ 		var loadVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var satisfyingVersion = findSatisfyingVersion(scope, key, requiredVersion, eager);
/******/ 			if (satisfyingVersion) return get(satisfyingVersion);
/******/ 			warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion, eager))
/******/ 			return get(findLatestVersion(scope, key, eager));
/******/ 		});
/******/ 		var loadStrictVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var satisfyingVersion = findSatisfyingVersion(scope, key, requiredVersion, eager);
/******/ 			if (satisfyingVersion) return get(satisfyingVersion);
/******/ 			if (fallback) return fallback();
/******/ 			fail(getInvalidVersionMessage(scope, scopeName, key, requiredVersion, eager));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key, eager, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var version = findSingletonVersionKey(scope, key, eager);
/******/ 			return get(scope[key][version]);
/******/ 		});
/******/ 		var loadSingletonVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var version = findSingletonVersionKey(scope, key, eager);
/******/ 			if (!satisfy(requiredVersion, version)) {
/******/ 				warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			}
/******/ 			return get(scope[key][version]);
/******/ 		});
/******/ 		var loadStrictSingletonVersion = /*#__PURE__*/ init((scopeName, scope, key, eager, requiredVersion, fallback) => {
/******/ 			if (!exists(scope, key)) return useFallback(scopeName, key, fallback);
/******/ 			var version = findSingletonVersionKey(scope, key, eager);
/******/ 			if (!satisfy(requiredVersion, version)) {
/******/ 				fail(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			}
/******/ 			return get(scope[key][version]);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			279: () => (loadSingletonVersion("default", "leaflet", false, [1,1,7,1], () => (__webpack_require__.e(862).then(() => (() => (__webpack_require__(3481))))))),
/******/ 			544: () => (loadStrictVersion("default", "spin.js", false, [1,4,1,0], () => (__webpack_require__.e(176).then(() => (() => (__webpack_require__(6176))))))),
/******/ 			1698: () => (loadStrictVersion("default", "leaflet.vectorgrid", false, [1,1,3,0], () => (__webpack_require__.e(256).then(() => (() => (__webpack_require__(4256))))))),
/******/ 			2176: () => (loadStrictVersion("default", "leaflet-search", false, [4,2,9,8], () => (Promise.all([__webpack_require__.e(844), __webpack_require__.e(104)]).then(() => (() => (__webpack_require__(9844))))))),
/******/ 			2276: () => (loadStrictVersion("default", "leaflet-draw", false, [1,1,0,4], () => (__webpack_require__.e(269).then(() => (() => (__webpack_require__(6269))))))),
/******/ 			2389: () => (loadStrictVersion("default", "leaflet.awesome-markers", false, [1,2,0,5], () => (__webpack_require__.e(268).then(() => (() => (__webpack_require__(4268))))))),
/******/ 			2730: () => (loadStrictVersion("default", "protomaps-leaflet", false, [1,1,24,0], () => (__webpack_require__.e(630).then(() => (() => (__webpack_require__(2630))))))),
/******/ 			4051: () => (loadStrictVersion("default", "leaflet-ant-path", false, [1,1,3,0], () => (Promise.all([__webpack_require__.e(512), __webpack_require__.e(224)]).then(() => (() => (__webpack_require__(2512))))))),
/******/ 			4062: () => (loadStrictVersion("default", "leaflet-velocity", false, [1,1,2,4], () => (__webpack_require__.e(464).then(() => (() => (__webpack_require__(2464))))))),
/******/ 			4176: () => (loadStrictVersion("default", "leaflet-splitmap", false, [1,1,0,3], () => (Promise.all([__webpack_require__.e(35), __webpack_require__.e(577)]).then(() => (() => (__webpack_require__(6958))))))),
/******/ 			4234: () => (loadStrictVersion("default", "leaflet-measure", false, [1,3,1,0], () => (__webpack_require__.e(380).then(() => (() => (__webpack_require__(380))))))),
/******/ 			4609: () => (loadStrictVersion("default", "leaflet-fullscreen", false, [1,1,0,2], () => (__webpack_require__.e(189).then(() => (() => (__webpack_require__(2189))))))),
/******/ 			4612: () => (loadStrictVersion("default", "@geoman-io/leaflet-geoman-free", false, [1,2,18,0], () => (__webpack_require__.e(10).then(() => (() => (__webpack_require__(5010))))))),
/******/ 			5256: () => (loadSingletonVersion("default", "@lumino/widgets", false, [1,2,3,1,,"alpha",0])),
/******/ 			5354: () => (loadStrictVersion("default", "proj4leaflet", false, [1,1,0,1], () => (Promise.all([__webpack_require__.e(481), __webpack_require__.e(761)]).then(() => (() => (__webpack_require__(7142))))))),
/******/ 			6230: () => (loadSingletonVersion("default", "@lumino/messaging", false, [1,2,0,0])),
/******/ 			6842: () => (loadStrictVersion("default", "leaflet-defaulticon-compatibility", false, [2,0,1,1], () => (__webpack_require__.e(320).then(() => (() => (__webpack_require__(939))))))),
/******/ 			7315: () => (loadStrictVersion("default", "leaflet-rotatedmarker", false, [2,0,2,0], () => (__webpack_require__.e(180).then(() => (() => (__webpack_require__(1180))))))),
/******/ 			7729: () => (loadStrictVersion("default", "proj4", false, [1,2,6,0], () => (__webpack_require__.e(363).then(() => (() => (__webpack_require__(363))))))),
/******/ 			8960: () => (loadStrictVersion("default", "leaflet-transform", false, [1,1,0,3], () => (Promise.all([__webpack_require__.e(94), __webpack_require__.e(35)]).then(() => (() => (__webpack_require__(2094))))))),
/******/ 			9181: () => (loadStrictVersion("default", "leaflet.markercluster", false, [1,1,2,0], () => (__webpack_require__.e(389).then(() => (() => (__webpack_require__(9389))))))),
/******/ 			4488: () => (loadSingletonVersion("default", "@jupyter-widgets/base", false, [,[1,6],[1,5],[1,4],[1,3],[1,2],1,1,1,1])),
/******/ 			9224: () => (loadSingletonVersion("default", "leaflet", false, [4,1,4,0], () => (__webpack_require__.e(862).then(() => (() => (__webpack_require__(3481))))))),
/******/ 			9104: () => (loadSingletonVersion("default", "leaflet", false, [0], () => (__webpack_require__.e(862).then(() => (() => (__webpack_require__(3481))))))),
/******/ 			8035: () => (loadSingletonVersion("default", "leaflet", false, [,[-1,2,0,0],[0,0,7,7],2], () => (__webpack_require__.e(862).then(() => (() => (__webpack_require__(3481))))))),
/******/ 			2481: () => (loadStrictVersion("default", "proj4", false, [1,2,3,14], () => (__webpack_require__.e(363).then(() => (() => (__webpack_require__(363)))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"35": [
/******/ 				8035
/******/ 			],
/******/ 			"104": [
/******/ 				9104
/******/ 			],
/******/ 			"224": [
/******/ 				9224
/******/ 			],
/******/ 			"279": [
/******/ 				279
/******/ 			],
/******/ 			"481": [
/******/ 				2481
/******/ 			],
/******/ 			"488": [
/******/ 				4488
/******/ 			],
/******/ 			"672": [
/******/ 				544,
/******/ 				1698,
/******/ 				2176,
/******/ 				2276,
/******/ 				2389,
/******/ 				2730,
/******/ 				4051,
/******/ 				4062,
/******/ 				4176,
/******/ 				4234,
/******/ 				4609,
/******/ 				4612,
/******/ 				5256,
/******/ 				5354,
/******/ 				6230,
/******/ 				6842,
/******/ 				7315,
/******/ 				7729,
/******/ 				8960,
/******/ 				9181
/******/ 			]
/******/ 		};
/******/ 		var startedInstallModules = {};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					if(!startedInstallModules[id]) {
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					startedInstallModules[id] = true;
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 					}
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		__webpack_require__.b = document.baseURI || self.location.href;
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			43: 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^(48[18]|104|224|279|35)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkjupyter_leaflet_bis"] = self["webpackChunkjupyter_leaflet_bis"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__(7536);
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB)["jupyter-leaflet-bis"] = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.0b54bb5af158f4054663.js.map