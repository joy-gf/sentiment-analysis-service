# Lista de Tareas

## ✅ HECHO

- [x] Servicio básico funcionando
- [x] Endpoint para analizar texto
- [x] Responde positivo/negativo/neutral
- [x] Documentación automática en /docs

## 📋 POR HACER

### Inmediato (Sprint 2)
- [ ] Conectar con el backend Express
- [ ] Guardar resultados en PostgreSQL
- [ ] Probar que funciona de punta a punta

### Después
- [ ] Analizar varios textos a la vez (batch)
- [ ] Extraer palabras clave del texto
- [ ] Detectar emociones específicas (alegría, tristeza, enojo, etc)

### Cuando sea necesario
- [ ] Caché (Redis) si es muy lento con muchos usuarios
- [ ] Docker para deployment más fácil

## 📝 Decisiones

- **No hay tests:** Prioridad en funcionalidad
- **Solo CPU:** GPU es opcional
- **Sin caché todavía:** 30 pacientes no lo necesitan
- **Simple:** Solo lo necesario
