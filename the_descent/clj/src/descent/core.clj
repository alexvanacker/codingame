(ns descent.core
  (:gen-class))

                                        ; The while loop represents the game.
                                        ; Each iteration represents a turn of the game
                                        ; where you are given inputs (the heights of the mountains)
                                        ; and where you have to print an output (the index of the mountain to fire on)
                                        ; The inputs you are given are automatically updated according to your last actions.


(defn -main [& args]
  (while true
    (println
     (loop [i 0 max_height_index -1 max_height -1]
       (if (= i 8) max_height_index
           (let [mountainH (read)]
             (binding [*out* *err*] (println (str "Index "i" Height " mountainH)))
             (when (> mountainH max_height) (binding [*out* *err*] (println (str "New max height "mountainH" found at index "i))))
             (recur (inc i) (if (> mountainH max_height) i max_height_index) (if (> mountainH max_height) mountainH max_height))))))))
