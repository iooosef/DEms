<template>
  <NewEntry id="new-entry" @new-entry-close="btnNewEntryClosed" v-if="btnNewEntryState" 
    :fetchedDBfamilies="fetchedDBfamilies"
    :newEntryEvacInfo="newEntryEvacInfo"
    :btnNewEntryState="btnNewEntryState"
    :fetchedEvacInfo="fetchedEvacInfo" />
  <MainApp id="main-app" 
    @new-entry="btnNewEntryClicked" @evac-info="btnEvacInfoChange" @change-table="fetch_data_fromPy"
    :fetchedEvacInfo="fetchedEvacInfo"  
    :fetchedDBevac="fetchedDBevac" 
    :fetchedDBfamilies="fetchedDBfamilies"
    :fetchedDBmed="fetchedDBmed"
    :fetchedDBrelief="fetchedDBrelief"
    :statsEvacInfo="statsEvacInfo" />
</template>

<script>
import MainApp from './components/Main.vue'
import NewEntry from './components/NewEntry.vue'

export default {
  name: 'App',
  components: {
    MainApp,
    NewEntry
  },
  data() {
    return {
      btnNewEntryState: false,

      fetchedDBevac: '',
      fetchedDBfamilies: '',
      fetchedDBmed: '',
      fetchedDBrelief: '',

      fetchedEvacInfo: '',
      newEntryEvacInfo: '',
      statsEvacInfo: ''
    }
  },
  created () {    
        window.addEventListener('beforeunload', this.windowClose)
  },  
  methods: {
    windowClose() {
      console.log("closing...")
      window.eel.sqlitecloseConnection();
    },
    async fetch_data_fromPy() { // receive data from python
        const dataFetched = await window.eel.passDB_toJS()()
        const evacInfo = await window.eel.passEvacInfo_toJS()()      
        const statsInfo = await window.eel.passStatsInfo_toJS()()
        this.fetchedDBevac = JSON.parse(dataFetched['db_evacuees'])      
        this.fetchedDBfamilies = JSON.parse(dataFetched['db_families'])      
        this.fetchedDBmed = JSON.parse(dataFetched['db_medAssist'])      
        this.fetchedDBrelief = JSON.parse(dataFetched['db_relief'])
        this.fetchedEvacInfo = evacInfo
        this.statsEvacInfo = statsInfo
    },
    btnNewEntryClicked() {
      this.btnNewEntryState = true
      this.newEntryEvacInfo = false
    },
    btnNewEntryClosed() {
      this.btnNewEntryState = false
      this.newEntryEvacInfo = false
    },
    btnEvacInfoChange() {
      this.btnNewEntryState = true
      this.newEntryEvacInfo = true
    },
    drpDownOptionsUpdate(currentData, currentField, currentTable) {
      let drpDownOptions = [];
      if(currentTable === 'Families Table' || 
          (currentTable === 'Medical Reports Table' && currentField === 'evacID') ||
          (currentTable === 'Relief Operations Table' && currentField === 'reliefRep')) {
        drpDownOptions = []
        for (const row of this.fetchedDBevac) {
          currentData.famID === row.famID ? 
            drpDownOptions.push( {label: `ID No. ${row.evacID} of ${row.fName} ${row.lName}`, value: row.evacID}) : ''
        }
      } else if(currentTable === 'Evacuees Table' || 
        (currentTable === 'Medical Reports Table' && currentField === 'famID')) {
        drpDownOptions = []
        for (const row of this.fetchedDBfamilies) {
          !this.fetchedDBevac.find(({evacID}) => evacID === row.famCID) ? 
          drpDownOptions.push({label: `Family no. ${row.famID}: ${row.famName} Family`,
            value: row.famID}) : 
          drpDownOptions.push({label: `Family no. ${row.famID} with 
            ${this.fetchedDBevac.find(({evacID}) => evacID === row.famCID).fName} 
            ${this.fetchedDBevac.find(({evacID}) => evacID === row.famCID).lName}`,
            value: row.famID})
        } 
      } else if(currentTable === 'Relief Operations Table' && currentField === 'reliefStatus') {
        drpDownOptions = []
        drpDownOptions.push({label: `received`, value: 1})
        drpDownOptions.push({label: `not received`, value: 0})
      }
      else if(currentTable === 'Families Table' || 
          (currentTable === 'Medical Reports Table' && currentField === 'evacID') ||
          (currentTable === 'Relief Operations Table' && currentField === 'evacID')) {
        drpDownOptions = []
        for (const row of this.fetchedDBevac) {
          currentData.famID === row.famID ? 
            drpDownOptions.push( {label: `ID No. ${row.evacID}: ${row.fName} ${row.lName}`, value: row.evacID}) : ''
        }
      }
      return drpDownOptions
    },
    
  }
}
</script>

<style>
#new-entry {
  position: absolute;
  z-index: 10;
}

#main-app {
  z-index: 1;
}
</style>
