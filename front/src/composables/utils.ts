import { useData } from 'stores/useData'
import { ITicker } from 'components/models'
import { computed, toRefs } from 'vue'


const data = useData()

export function useTickersByExchange(exchange: string, tickers: Array<ITicker>) {
  if (tickers !== null) {
    const dataExchange = tickers.filter(ticker => ticker.exchange === exchange)
    console.log('resultado do filter per exchange: ', dataExchange)
    return dataExchange
  }
}

export function useTickersByCoin(coin: string = 'btcbrl', tickers: Array<ITicker>) {
  if (tickers !== null) {
    const dataCoin = tickers.filter(ticker => ticker.cripto === coin)
    console.log('resultado do filter per exchange: ', dataCoin)
    return dataCoin
  }
}

export function useTickersByCoinTest(coin: string = 'btcbrl') {
  const tickersFinal = computed(() => {
    const tickers = data.getTickers
    if (tickers !== null) {
      const dataCoin = tickers.filter(ticker => ticker.cripto === coin)
      console.log('resultado do filter per exchange: ', dataCoin)
      return dataCoin
    }
  })
  return toRefs(tickersFinal)
}
