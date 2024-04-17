package main

import (
	"fmt"
	"sync"
)

var (
	AllRedisDb = make(map[int64]string) // redis对外服务Obj
	wg         sync.WaitGroup
	mutex      sync.Mutex
)

func main() {
	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go readMap(i)
	}

	wg.Wait()
}

func readMap(index int) {
	defer wg.Done()
	mutex.Lock()
	mutex.Unlock()

	// 在读取 map 时，如果没有加锁保护，会存在线程安全问题
	fmt.Printf("Index: %d, Value: %s\n", index, AllRedisDb[int64(index)])
}
