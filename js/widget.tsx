import * as React from "react";
import { createRender, useModelState } from "@anywidget/react";
import "./widget.css";

const SequenceComponent = ({ c, participantSequencesCount, max, sum }: { c: any, participantSequencesCount: { [key: string]: number }, max: number, sum: number }) => {
  return (<div className="sequenceComponent">
    {typeof c === "string" ? <div className="sequenceComponentIndividual" title={`${c} = ${participantSequencesCount[c] / max}`} style={{ opacity: participantSequencesCount[c] / max }} /> :
      (<>{c.components.map((ci: any, idx: number) => <SequenceComponent key={idx} c={ci} participantSequencesCount={participantSequencesCount} max={max} sum={sum} />)}</>)}
  </div>);
}

const getFlattenedSequenceList = (d: any[]): any[] => {
  return d.map((a: any) => typeof a === "string" ? a : getFlattenedSequenceList(a.components).flat());
};


function extractInterruptions(d: any) {
  let interruptions: string[] = [];

  // Recursive function to traverse the JSON object
  function traverse(node: any) {
      // Check if the current node has interruptions
      if (node.interruptions) {
          node.interruptions.forEach((interruption: any) => {
              if (interruption.components) {
                  interruptions.push(...interruption.components);
              }
          });
      }

      // Check if the current node has components and process them recursively
      if (Array.isArray(node.components)) {
          node.components.forEach((component: any) => {
              if (typeof component === "object") {
                  traverse(component);
              }
          });
      }
  }

  // Start traversal from the root JSON object
  traverse(d);

  return interruptions;
}

const Sequence = ({ d, participantSequences }: { d: any, participantSequences: any[] }) => {
  const [participantSequencesCount, max, sum] = React.useMemo(() => {
    const r: { [key: string]: number } = {};

    
    if (participantSequences.length) {
      const allStimuli = getFlattenedSequenceList(participantSequences).flat();

      const interruptions = extractInterruptions(d);
      console.log(interruptions);


      allStimuli.forEach((s: string) => {
        if (!r[s]) {
          r[s] = 0;
        }
        r[s]++;
      });

      for (let i = 0; i < interruptions.length; i++) {
        // check if key is in r
        if (interruptions[i] in r) {
          delete r[interruptions[i]];
        }

        // if (!r[interruptions[i]]) {
        //   r[interruptions[i]] = 0;
        // }
        // r[interruptions[i]]++;
      }

    }

    const sum = Object.values(r).reduce((acc, v) => acc + v, 0);

    const max = Math.max(...Object.values(r));

    // console.log(r, max, sum);
    // console.log(d);

    return [r, max, sum];
  
  }, [participantSequences]);

  return (<div className="sequence">
    {d.components.map((c: any, idx: number) => <SequenceComponent key={idx} c={c} participantSequencesCount={participantSequencesCount} max={max} sum={sum} />)}
  </div>);
};

const render = createRender(() => {
  // TODO: replace with revisit configuration
  const [config] = useModelState<any>("config");
  const [iframeReady, setIframeReady] = React.useState(0);
  const [sequences, setSequence] = useModelState<any>("sequence");


  const ref = React.useRef<HTMLIFrameElement>(null);

  React.useEffect(() => {
    if (iframeReady) {
      ref.current?.contentWindow?.postMessage(
        {
          type: "revisitWidget/CONFIG",
          payload: JSON.stringify(config),
        },
        "http://localhost:8080"
      );
    }
  }, [config, iframeReady]);

  React.useEffect(() => {
    const messageListener = (event: MessageEvent) => {
      if (event.data.type === "revisitWidget/READY") {
        setIframeReady(i => i + 1);
      } else if (event.data.type === "revisitWidget/SEQUENCE_ARRAY") {
        // console.log(event.data.payload);
        setSequence(event.data.payload);
      }
    };

    window.addEventListener("message", messageListener);

    return () => {
      window.removeEventListener("message", messageListener);
    };
  }, [config]);

  return (
    <div className="revisit_notebook_widget">
      <Sequence d={config.sequence} participantSequences={sequences} />
      <iframe
        ref={ref}
        src="http://localhost:8080/revisit-widget"
        style={{ width: "100%", height: "400px" }}
      />
    </div>
  );
});

export default { render };
