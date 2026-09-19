<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { delJSON, getJSON, postJSON } from '../api'

const route = useRoute()
const router = useRouter()
const rec = ref(null)
const stations = ref([])
const current = ref(null) // fresh read-only quote against the CURRENT graph
const error = ref('')

const names = computed(() => Object.fromEntries(stations.value.map(s => [s.code, s.name])))
const label = (code) => (names.value[code] ? `${code} ${names.value[code]}` : code)

onMounted(async () => {
  const [item, st] = await Promise.all([
    getJSON(`/api/history/${route.params.id}`),
    getJSON('/api/stations'),
  ])
  rec.value = item
  stations.value = st.items
})

// Locked snapshot fields — served verbatim from the record, never recomputed.
const locked = computed(() => rec.value?.result ?? {})
// Records written before path-locking existed have no path; fall back to empty.
const lockedPath = computed(() => locked.value.path ?? [])

// Re-quote from this record: read-only (persist=false), hits the current graph,
// and never writes back into this record.
const requote = async () => {
  error.value = ''
  try {
    current.value = await postJSON('/api/quote', {
      start: rec.value.input.start,
      end: rec.value.input.end,
      persist: false,
    })
  } catch (e) {
    error.value = String(e)
  }
}

const differs = computed(() => {
  if (!current.value || !current.value.reachable) return false
  return current.value.hops !== locked.value.hops
    || current.value.fare !== locked.value.fare
    || JSON.stringify(current.value.path) !== JSON.stringify(locked.value.path)
})

const remove = async () => {
  await delJSON(`/api/history/${rec.value.id}`)
  router.push('/history')
}
</script>

<template>
  <div class="page" v-if="rec">
    <h1>记录 #{{ rec.id }}</h1>

    <div class="panel">
      <p class="muted">锁定快照 · {{ rec.created_at }} · 此后增删边、改票价均不影响本记录</p>
      <p>{{ locked.start }} → {{ locked.end }}</p>
      <template v-if="locked.reachable">
        <p class="path" v-if="lockedPath.length">
          <template v-for="(code, i) in lockedPath" :key="i">
            <span v-if="i"> → </span><span class="stop">{{ label(code) }}</span>
          </template>
        </p>
        <p>站数 {{ locked.hops }} · 票价 <span class="hero-num">¥{{ locked.fare }}</span></p>
      </template>
      <p v-else class="muted">不可达</p>
      <button @click="requote">按当前图重新试算</button>
      <button class="danger" @click="remove">删除记录</button>
    </div>

    <div v-if="current" class="panel current">
      <p class="muted">当前图试算 · 只读，不写回本记录</p>
      <template v-if="current.reachable">
        <p class="path">
          <template v-for="(code, i) in current.path" :key="i">
            <span v-if="i"> → </span><span class="stop">{{ label(code) }}</span>
          </template>
        </p>
        <p>站数 {{ current.hops }} · 票价 <span class="hero-num">¥{{ current.fare }}</span></p>
        <p v-if="differs" class="warn">与锁定快照不同（线网或票价已变化）</p>
        <p v-else class="muted">与锁定快照一致</p>
      </template>
      <p v-else class="muted">当前图不可达</p>
    </div>
    <p v-if="error" class="warn">{{ error }}</p>
  </div>
</template>

<style scoped>
.path { line-height: 1.9; }
.stop { white-space: nowrap; }
.current { border: 1px dashed var(--muted); }
.warn { color: #ffb454; }
.danger { background: #c0392b; color: #fff; margin-left: 0.5rem; }
</style>
