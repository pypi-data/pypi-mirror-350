const crypto = {
    randomBytes(size) {
      if (typeof size !== 'number' || size < 0)
        throw new TypeError('size must be a non-negative number')
  
      const buffer = new Uint8Array(size)
      for (let i = 0; i < size; i++)
        buffer[i] = Math.floor(Math.random() * 256)
  
      return {
        buffer,
        toString(encoding) {
          if (encoding === 'hex')
            return Array.from(buffer).map(b => b.toString(16).padStart(2, '0')).join('')
          if (encoding === 'base64')
            return btoa(String.fromCharCode(...buffer))
          throw new Error(`Encoding "${encoding}" not supported`)
        }
      }
    },
  
    getRandomValues(typedArray) {
      if (!ArrayBuffer.isView(typedArray) || !(typedArray instanceof Uint8Array))
        throw new TypeError('Expected a Uint8Array or similar TypedArray')
  
      for (let i = 0; i < typedArray.length; i++)
        typedArray[i] = Math.floor(Math.random() * 256)
  
      return typedArray
    },
  
    // Polyfill para randomFillSync con la definición correcta
    randomFillSync(buffer, offset = 0, size = buffer.length - offset) {
      if (!(buffer instanceof Uint8Array)) {
        throw new TypeError('First argument must be a Uint8Array')
      }
  
      if (typeof offset !== 'number' || offset < 0 || offset >= buffer.length) {
        throw new RangeError('Offset out of bounds')
      }
  
      if (typeof size !== 'number' || size < 0 || offset + size > buffer.length) {
        throw new RangeError('Invalid size or buffer overflow')
      }
  
      // Llenamos el buffer con valores aleatorios
      for (let i = offset; i < offset + size; i++) {
        buffer[i] = Math.floor(Math.random() * 256)
      }
  
      return buffer
    }
  }
  
  module.exports = crypto
  