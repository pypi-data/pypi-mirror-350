globalThis.process = {
    env: {},

    nextTick(callback, ...args) {
        Promise.resolve().then(() => callback(...args))
    },

    version: 'v18.0.0',
    versions: {
        node: '18.0.0'
    },

    cwd() {
        return '/'
    },

    browser: false,
    platform: 'browser',
    argv: [],
    stdout: {
        write: (msg) => console.log(msg)
    },
    stderr: {
        write: (msg) => console.error(msg)
    }
}
  
const { Evaluation, fromJSON, interprete, Interpreter, link, parse, REPL, WOLLOK_FILE_EXTENSION, WRE, WRENatives } = require("wollok-ts")

const replPackage = parse.File(REPL + '.' + WOLLOK_FILE_EXTENSION).tryParse("object pepita {}")
const environment = link([replPackage], fromJSON(WRE))
const interpreter = new Interpreter(Evaluation.build(environment, WRENatives))

const successDescription = (result) => '✓ ' + result

const sanitizeStackTrace = (e) => e.message.replace("Derived from TypeScript stack", "").trim()

const failureDescription = (result, error) => {
    const stack = sanitizeStackTrace(error)
    const sanitizedStackTrace = stack ? '\n  ' + stack : ''
    return `✗ ${result}${sanitizedStackTrace}`
}

function repl(expression) {
    const { error, errored, result} = interprete(interpreter, expression)
    return errored ? failureDescription(result, error) : successDescription(result)
}

module.exports = {
    repl
}
