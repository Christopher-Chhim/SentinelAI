/**
 * Unit tests for lib/utils.ts
 * 
 * Tests the cn utility function for className merging.
 */

import { cn } from '@/lib/utils'

describe('cn utility function', () => {
  describe('Basic functionality', () => {
    it('should merge single class name', () => {
      const result = cn('text-red-500')
      expect(result).toBe('text-red-500')
    })

    it('should merge multiple class names', () => {
      const result = cn('text-red-500', 'bg-blue-500')
      expect(result).toContain('text-red-500')
      expect(result).toContain('bg-blue-500')
    })

    it('should handle empty input', () => {
      const result = cn()
      expect(result).toBe('')
    })

    it('should handle undefined values', () => {
      const result = cn('text-red-500', undefined, 'bg-blue-500')
      expect(result).toContain('text-red-500')
      expect(result).toContain('bg-blue-500')
    })

    it('should handle null values', () => {
      const result = cn('text-red-500', null, 'bg-blue-500')
      expect(result).toContain('text-red-500')
      expect(result).toContain('bg-blue-500')
    })

    it('should handle false boolean values', () => {
      const result = cn('text-red-500', false && 'bg-blue-500')
      expect(result).toBe('text-red-500')
    })
  })

  describe('Conditional classes', () => {
    it('should apply conditional classes correctly', () => {
      const isActive = true
      const result = cn('base-class', isActive && 'active-class')
      expect(result).toContain('base-class')
      expect(result).toContain('active-class')
    })

    it('should not apply conditional classes when false', () => {
      const isActive = false
      const result = cn('base-class', isActive && 'active-class')
      expect(result).toBe('base-class')
      expect(result).not.toContain('active-class')
    })

    it('should handle ternary operators', () => {
      const isDanger = true
      const result = cn('button', isDanger ? 'text-red-500' : 'text-blue-500')
      expect(result).toContain('button')
      expect(result).toContain('text-red-500')
      expect(result).not.toContain('text-blue-500')
    })
  })

  describe('Tailwind class merging', () => {
    it('should merge conflicting Tailwind classes correctly', () => {
      // Later classes should override earlier ones
      const result = cn('p-4', 'p-8')
      expect(result).toBe('p-8')
    })

    it('should handle different types of spacing classes', () => {
      const result = cn('px-4', 'py-2')
      expect(result).toContain('px-4')
      expect(result).toContain('py-2')
    })

    it('should merge responsive classes', () => {
      const result = cn('text-sm', 'md:text-lg', 'lg:text-xl')
      expect(result).toContain('text-sm')
      expect(result).toContain('md:text-lg')
      expect(result).toContain('lg:text-xl')
    })

    it('should handle hover and focus states', () => {
      const result = cn('hover:bg-blue-500', 'focus:ring-2')
      expect(result).toContain('hover:bg-blue-500')
      expect(result).toContain('focus:ring-2')
    })
  })

  describe('Complex scenarios', () => {
    it('should handle arrays of classes', () => {
      const baseClasses = ['flex', 'items-center']
      const result = cn(...baseClasses, 'justify-between')
      expect(result).toContain('flex')
      expect(result).toContain('items-center')
      expect(result).toContain('justify-between')
    })

    it('should handle object notation', () => {
      const result = cn({
        'text-red-500': true,
        'text-blue-500': false,
      })
      expect(result).toContain('text-red-500')
      expect(result).not.toContain('text-blue-500')
    })

    it('should handle mixed inputs', () => {
      const isActive = true
      const result = cn(
        'base-class',
        { 'active': isActive },
        isActive && 'is-active',
        undefined,
        'final-class'
      )
      expect(result).toContain('base-class')
      expect(result).toContain('active')
      expect(result).toContain('is-active')
      expect(result).toContain('final-class')
    })

    it('should handle empty strings', () => {
      const result = cn('text-red-500', '', 'bg-blue-500')
      expect(result).toContain('text-red-500')
      expect(result).toContain('bg-blue-500')
    })

    it('should deduplicate identical classes', () => {
      const result = cn('text-red-500', 'text-red-500')
      // Should not duplicate the class
      const matches = result.match(/text-red-500/g)
      expect(matches).toHaveLength(1)
    })
  })

  describe('Status-based styling', () => {
    it('should apply danger status classes', () => {
      const status = 'danger'
      const result = cn(
        'zone',
        status === 'danger' && 'text-red-400',
        status === 'caution' && 'text-yellow-400',
        status === 'ok' && 'text-green-400'
      )
      expect(result).toContain('text-red-400')
      expect(result).not.toContain('text-yellow-400')
      expect(result).not.toContain('text-green-400')
    })

    it('should apply caution status classes', () => {
      const status = 'caution'
      const result = cn(
        'zone',
        status === 'danger' && 'text-red-400',
        status === 'caution' && 'text-yellow-400',
        status === 'ok' && 'text-green-400'
      )
      expect(result).toContain('text-yellow-400')
    })

    it('should apply ok status classes', () => {
      const status = 'ok'
      const result = cn(
        'zone',
        status === 'danger' && 'text-red-400',
        status === 'caution' && 'text-yellow-400',
        status === 'ok' && 'text-green-400'
      )
      expect(result).toContain('text-green-400')
    })
  })

  describe('Edge cases', () => {
    it('should handle very long class strings', () => {
      const longClasses = Array(50).fill('class').map((c, i) => `${c}-${i}`).join(' ')
      const result = cn(longClasses)
      expect(result).toBeDefined()
      expect(typeof result).toBe('string')
    })

    it('should handle special characters in class names', () => {
      const result = cn('sm:max-w-[425px]', 'data-[state=open]:animate-in')
      expect(result).toContain('sm:max-w-[425px]')
      expect(result).toContain('data-[state=open]:animate-in')
    })

    it('should return a string type', () => {
      const result = cn('class1', 'class2')
      expect(typeof result).toBe('string')
    })

    it('should not throw with unusual inputs', () => {
      expect(() => cn(0 as any)).not.toThrow()
      expect(() => cn(true as any)).not.toThrow()
    })
  })

  describe('Real-world usage patterns', () => {
    it('should work with button variants', () => {
      const variant = 'primary'
      const size = 'lg'
      const result = cn(
        'button',
        variant === 'primary' && 'bg-blue-500 text-white',
        variant === 'secondary' && 'bg-gray-500 text-white',
        size === 'sm' && 'text-sm px-2 py-1',
        size === 'lg' && 'text-lg px-4 py-2'
      )
      expect(result).toContain('button')
      expect(result).toContain('bg-blue-500')
      expect(result).toContain('text-lg')
    })

    it('should work with card states', () => {
      const isHovered = true
      const isSelected = false
      const result = cn(
        'card',
        'rounded-lg border',
        isHovered && 'shadow-lg',
        isSelected && 'border-blue-500'
      )
      expect(result).toContain('card')
      expect(result).toContain('shadow-lg')
      expect(result).not.toContain('border-blue-500')
    })

    it('should work with layout classes', () => {
      const result = cn(
        'flex',
        'flex-col',
        'items-center',
        'justify-center',
        'min-h-screen',
        'bg-gradient-to-b',
        'from-black',
        'to-slate-900'
      )
      expect(result).toContain('flex')
      expect(result).toContain('min-h-screen')
      expect(result).toContain('bg-gradient-to-b')
    })
  })
})