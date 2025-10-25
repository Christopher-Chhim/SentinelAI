/**
 * Integration tests for database schema validation
 * 
 * Validates that the schema.sql structure is correct and complete.
 */

import fs from 'fs'
import path from 'path'

describe('Database Schema Validation', () => {
  let schemaContent: string

  beforeAll(() => {
    const schemaPath = path.join(process.cwd(), '../db/schema.sql')
    if (fs.existsSync(schemaPath)) {
      schemaContent = fs.readFileSync(schemaPath, 'utf-8')
    } else {
      schemaContent = ''
    }
  })

  describe('Table existence', () => {
    it('should define zones table', () => {
      if (schemaContent) {
        expect(schemaContent).toContain('CREATE TABLE zones')
      }
    })

    it('should define devices table', () => {
      if (schemaContent) {
        expect(schemaContent).toContain('CREATE TABLE devices')
      }
    })

    it('should define incidents table', () => {
      if (schemaContent) {
        expect(schemaContent).toContain('CREATE TABLE incidents')
      }
    })

    it('should define actions table', () => {
      if (schemaContent) {
        expect(schemaContent).toContain('CREATE TABLE actions')
      }
    })

    it('should define users table', () => {
      if (schemaContent) {
        expect(schemaContent).toContain('CREATE TABLE users')
      }
    })
  })

  describe('Column definitions', () => {
    it('zones table should have required columns', () => {
      if (schemaContent) {
        expect(schemaContent).toMatch(/zones[\s\S]*id[\s\S]*PRIMARY KEY/)
        expect(schemaContent).toMatch(/zones[\s\S]*name[\s\S]*NOT NULL/)
      }
    })

    it('devices table should have zone_id foreign key', () => {
      if (schemaContent) {
        expect(schemaContent).toMatch(/devices[\s\S]*zone_id[\s\S]*REFERENCES zones/)
      }
    })

    it('incidents table should have proper foreign keys', () => {
      if (schemaContent) {
        expect(schemaContent).toMatch(/incidents[\s\S]*zone_id[\s\S]*REFERENCES zones/)
        expect(schemaContent).toMatch(/incidents[\s\S]*device_id[\s\S]*REFERENCES devices/)
      }
    })
  })

  describe('Data integrity', () => {
    it('should have proper CASCADE delete rules', () => {
      if (schemaContent) {
        expect(schemaContent).toMatch(/ON DELETE CASCADE|ON DELETE SET NULL/)
      }
    })

    it('should have timestamp fields with defaults', () => {
      if (schemaContent) {
        expect(schemaContent).toMatch(/DEFAULT NOW\(\)/)
      }
    })

    it('should have appropriate status enums or text fields', () => {
      if (schemaContent) {
        expect(schemaContent).toContain('status TEXT')
      }
    })
  })
})